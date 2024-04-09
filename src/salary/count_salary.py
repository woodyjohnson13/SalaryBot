#{'days': '15', 'sum': '567000', 'service': 'Да'}

class Salary:

    def count_all(self, data_bot: dict):
        day = data_bot["days"]
        day = int(day)
        numb = data_bot["summ"]
        numb = int(numb) // 100 * 3
        serv = data_bot["service"]
        if serv.lower() == "да":
            return str(day * 2100 + numb)
        else: 
            return str(day * 1800 + numb)

