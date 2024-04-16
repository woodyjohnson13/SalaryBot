class Salary:

    def count_all(self, data_bot: dict):
        day = data_bot["days"]
        day = int(day)
        summ = data_bot["summ"]
        summ = int(summ) // 100 * 3
        serv = data_bot["service"]
        if serv.lower() == "да":
            return str(day * 2100 + summ)
        else: 
            return str(day * 1960 + summ)
        
    def count_every(self, data_bot):
        day = data_bot["days"]
        day = int(day)
        summ_every = data_bot["summ_every"]
        count_summ = data_bot["count_summ"]
        count_summ = int(count_summ)
        summ_every = int(summ_every)
        full_summ = (count_summ + summ_every) // 100 * 3
        serv = data_bot["service_every"]
        if serv.lower() == "да":
            return str(day * 2100 + full_summ)
        else: 
            return str(day * 1960 + full_summ)


