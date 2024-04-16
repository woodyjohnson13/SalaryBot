class Test:
    def int_test(self, data_bot: str) -> bool:
        if data_bot.isdigit() and data_bot != "0":
            return True
        return False


    def str_test(self, data_bot: str) -> bool:
        if not data_bot.isdigit() and data_bot != "0":
            return True
        return False
    
    def anwswer_test(self, data_bot: str) -> bool:
        answer_list = ["да", "нет"]
        if data_bot.lower() in answer_list:
            return True
        return False