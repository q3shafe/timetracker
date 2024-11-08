# readpkl.py
import pickle

with open('time_tracker_state.pkl', 'rb') as p_f:
    data = pickle.load(p_f)

print(data)
