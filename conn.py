import abc
import multiprocessing


class BaseConnection(abc.ABC):
    @abc.abstractmethod
    def connect(self, ident: str) -> bool:
        pass

    @abc.abstractmethod
    def disconnect(self) -> bool:
        pass

    @abc.abstractmethod
    def write_bytes(self, b: bytes) -> None:
        pass

    @abc.abstractmethod
    def read_bytes(self) -> bytes | None:
        pass


class SerialConnection(BaseConnection):
    def __init__(self) -> None:
        self.abort_event = multiprocessing.Event()
        self.abort_event.clear()

        self.stop_event = multiprocessing.Event()
        self.stop_event.clear()

        self.pp, self.cp = multiprocessing.Pipe(True)

        self.p: multiprocessing.Process | None = None

    def connect(self, ident: str) -> bool:
        if self.p is None:
            self.p = multiprocessing.Process(target=self.connection, args=(ident,))
            self.p.start()
        return True

    def disconnect(self) -> bool:
        self.stop_event.set()
        if self.p is not None:
            self.p.join()
        return True

    def is_abort(self) -> bool:
        return self.abort_event.is_set()

    def write_bytes(self, b: bytes):
        self.pp.send(b)

    def read_bytes(self) -> bytes | None:
        return self.pp.recv() if self.pp.poll(1) else None

    def connection(self, ident: str) -> None:
        # connect
        import serial

        s = serial.Serial(port=ident, baudrate=115200, timeout=1)
        if not s.is_open:
            self.abort_event.set()
            return

        # communication loop
        while not self.stop_event.is_set():
            s.write(self.cp.recv())
            self.cp.send(s.read(1))


class ConnectionManager:
    def __init__(self):
        pass
