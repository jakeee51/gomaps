import gomaps, time

if __name__ == "__main__":
   t0 = time.process_time()

   results = gomaps.maps_search("Tops Diner, NJ", single=True)
   values = results.get_values()
   for val in values.values():
      print(val)
      assert val == None or val == {}, "Gomaps results missing values!"
   results = gomaps.maps_search("Tops Diner, NJ", fields=["coords", "rating"])
   print(results.values)
   assert len(results.values) == 2, "Gomaps fields feature failed!"


##   results = gomaps.get_url("Tops Diner, NJ")
##   print(results)
##   assert results != None, "Gomaps could not find the requested url!"
##   results = gomaps.get_address("331 River Road, NJ 07646")
##   print(results)
##   assert results != None, "Gomaps could not find the requested address!"
##   results = gomaps.geocoder("Tops Diner")
##   print(results)
##   assert results != None, "Gomaps could not geocode this location!"

   t1 = time.process_time()
   total = t1 - t0
   print(f"\nTimestamp 1: {t0} secs\nTimestamp 2: {t1} secs")
   print("Module Time Elapsed:", total, "seconds")
