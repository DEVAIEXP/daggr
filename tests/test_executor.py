from daggr import FnNode, Graph
from daggr.executor import SequentialExecutor


class TestSequentialExecutor:
    def test_execute_single_fn_node(self):
        def double(x):
            return {"result": x * 2}

        node = FnNode(double, inputs={"x": 5})
        graph = Graph("test", nodes=[node])
        executor = SequentialExecutor(graph)
        result = executor.execute_node("double", {})
        assert result["result"] == 10

    def test_execute_chain(self):
        def step1(x):
            return {"output": x + 1}

        def step2(y):
            return {"output": y * 2}

        n1 = FnNode(step1, inputs={"x": 10})
        n2 = FnNode(step2, inputs={"y": n1.output})
        graph = Graph("test", nodes=[n2])
        executor = SequentialExecutor(graph)
        executor.execute_node("step1", {})
        result = executor.execute_node("step2", {})
        assert result["output"] == 22

    def test_execute_all(self):
        def add_one(x):
            return {"output": x + 1}

        def double(x):
            return {"output": x * 2}

        n1 = FnNode(add_one, name="add_one", inputs={"x": 3})
        n2 = FnNode(double, name="double", inputs={"x": n1.output})
        graph = Graph("test", nodes=[n2])
        executor = SequentialExecutor(graph)
        results = executor.execute_all({})
        assert results["add_one"]["output"] == 4
        assert results["double"]["output"] == 8

    def test_fn_result_mapping(self):
        def multi_output(x):
            return {"first": x, "second": x * 2}

        node = FnNode(
            multi_output, inputs={"x": 5}, outputs={"first": None, "second": None}
        )
        graph = Graph("test", nodes=[node])
        executor = SequentialExecutor(graph)
        result = executor.execute_node("multi_output", {})
        assert result["first"] == 5
        assert result["second"] == 10

    def test_user_input_override(self):
        def process(text):
            return {"out": text.upper()}

        node = FnNode(process, inputs={"text": "default"})
        graph = Graph("test", nodes=[node])
        executor = SequentialExecutor(graph)
        result = executor.execute_node("process", {"text": "hello"})
        assert result["out"] == "HELLO"

    def test_callable_fixed_input(self):
        counter = {"value": 0}

        def get_next():
            counter["value"] += 1
            return counter["value"]

        def process(x):
            return {"out": x}

        node = FnNode(process, inputs={"x": get_next})
        graph = Graph("test", nodes=[node])
        executor = SequentialExecutor(graph)
        result1 = executor.execute_node("process", {})
        result2 = executor.execute_node("process", {})
        assert result1["out"] == 1
        assert result2["out"] == 2
