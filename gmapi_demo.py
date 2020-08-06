import gmapi, time

if __name__ == "__main__":
   t0 = time.process_time()

##   print(gmapi.popular_times("Star Diner, White Plains, NY"))
##   result = gmapi.maps_search("Tops Diner", single=True)
##   print(result.get_values())

   t1 = time.process_time()
   total = t1 - t0
   print(f"Timestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
   print("Module Time Elapsed:", total, "seconds")
# 0.046875 seconds, 0.015625 seconds
# 0.5 seconds, 0.4375 seconds
