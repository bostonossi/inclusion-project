import inspect
import pkgutil


class Engine:

    def __init__(self, path):
        self.collectors = []
        self.load_collectors(path)

    def load_collectors(self, path):
        collectors = __import__(path, fromlist=[''])
        plugins = pkgutil.iter_modules(collectors.__path__, collectors.__name__ + '.')
        for _, plname, ispkg in plugins:
            if not ispkg:
                plugin_module = __import__(plname, fromlist=[''])
                children = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, cls) in children:
                    # TODO Replace none with base collector class
                    if issubclass(cls, None) & (cls is not None):
                        self.collectors.append(cls())

    def run(self):
        for collector in self.collectors:
            collector.run()
