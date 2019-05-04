import functions

func = functions.load_func()

canceled_shows = func.load_json("canceled.json")
renewed_shows = func.load_json("renewed.json")
rescued_shows = func.load_json("rescued.json")

func.tv_show_data = []
func.imdb_reviews = []

for i in rescued_shows:
    func.get_imdb_data(i)
func.write_json('rescued')
func.write_json('rescued_reviews')

func.tv_show_data = []
func.imdb_reviews = []

for i in renewed_shows:
    func.get_imdb_data(i)
func.write_json('renewed')
func.write_json('renewed_reviews')

func.tv_show_data = []
func.imdb_reviews = []

for i in canceled_shows:
    func.get_imdb_data(i)
func.write_json('canceled')
func.write_json('canceled_reviews')
