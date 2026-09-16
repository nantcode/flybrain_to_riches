import flybrain

# Initialize the FlyBrain model with downloaded data
b = flybrain.FlyBrain("/Users/anthonymac/fly-data")
print("Fly brain loaded successfully!")

# Run the simulation engine
res = flybrain.run(b, steps=100)
print(f"Simulation completed! Readout shape: {res}")
