from expression import Error

class CloseTask:
    def execute(self) -> None:
        pass




class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        pass
        # assert CloseTask().execute() == Error()