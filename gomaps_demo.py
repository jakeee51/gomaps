import gmapi, time

if __name__ == "__main__":
   t0 = time.process_time()

##   print(gmapi.popular_times("Tops Diner", "chromedriver.exe"))
   result = gmapi.maps_search("Tops Diner")
   print(result)

   t1 = time.process_time()
   total = t1 - t0
   print(f"Timestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
   print("Module Time Elapsed:", total, "seconds")
