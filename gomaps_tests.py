import gomaps, time

if __name__ == "__main__":
   t0 = time.process_time()

   results = gomaps.maps_search("Tops Diner, NJ")
   print(results)
   values = results[0].get_values()
   for val in values.values():
      print(val)
      assert val != None or val != {}, "Gomaps results missing values!"
   results = gomaps.maps_search("Tops Diner, NJ", fields=["coords", "rating"])
   print(results.values)
   assert len(results.values) == 2, "Gomaps fields feature failed!"

   t1 = time.process_time()
   total = t1 - t0
   print(f"\nTimestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
   print("Module Time Elapsed:", total, "seconds")
