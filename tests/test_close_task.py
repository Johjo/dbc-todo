class CloseTask:
    pass


class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        CloseTask()