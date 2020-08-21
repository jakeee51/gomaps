import gomaps, time

if __name__ == "__main__":
   t0 = time.process_time()

   results = gomaps.maps_search("Tops Diner, NJ", single=True)
   print(results.get_values())

   t1 = time.process_time()
   total = t1 - t0
   print(f"Timestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
   print("Module Time Elapsed:", total, "seconds")
