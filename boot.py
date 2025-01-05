import machine
# app.run()



if machine.reset_cause() == machine.SOFT_RESET:
   print("Safe mode enabled. Skipping boot.py execution.")
else:
   import main
   main.main()
