from anxiety_module import AnxietyModel

m=AnxietyModel(20)
m.add_stressor(motion_type='strong vibration',freq=2.0,amplitude=15.0,lag=0.0,burst_start_time=100.0,burst_freq=50.0,impulse_magnitude=0.0,duration=0.50,risk_factor=1.0)
m.add_stressor(motion_type='sudden stop',start_time=600.0,freq=2.0,amplitude=2.0,lag=0.0,burst_start_time=60.0,burst_freq=50.0,impulse_magnitude=10.0,duration=0.01,risk_factor=4.0,decay=0.01)

for i,s in enumerate(m.stressor_history):
    print('---')
    print('anxiety',m.anxiety_history[i].level, ' anxiety time',m.anxiety_history[i-1].time)
    print('type', s.motion_type)
    print('time', s.time, 'dur', s.duration)
    print('jerk_mag', s.magnitude)
    print('kurt', s.unexpectedness)
    print('surprise', s.surprise)
    print('crest', s.crest)