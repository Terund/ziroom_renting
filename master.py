from redis import Redis


r = Redis()
count = 0
with open("area.txt", "r", encoding="utf-8") as fp:
    content = fp.read().strip()
city_list = content.split("\n")

for city_url in city_list:
    r.lpush('renting:start_url', city_url)
    count += 1
    print(city_url)
r.set("total_task", count)
