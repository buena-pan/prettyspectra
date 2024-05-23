# CASA Script Example for Simulating Astronomical Signals

import casatools
import casatasks

# Initialize the simulator
sm = casatools.simulator()

# Define the number of antennas and their positions (example for 4 antennas)
num_antennas = 4
positions = [[0, 0, 0], [100, 0, 0], [0, 100, 0], [100, 100, 0]]

# Set the antenna configuration
sm.open('simulation.ms')
sm.setconfig(telescopename='VLA', x=[pos[0] for pos in positions],
             y=[pos[1] for pos in positions], z=[pos[2] for pos in positions],
             dishdiameter=[25] * num_antennas, mount=['ALT-AZ'] * num_antennas,
             coordsystem='local', referencelocation=[-30, 70])

# Define the field (source)
sm.setfield(sourcename='TestSource', sourcedirection=['J2000', '19h00m00', '-40d00m00'])

# Define the spectral window
sm.setspwindow(spwname='TestSPW', freq='1.5GHz', deltafreq='50MHz', freqresolution='50MHz', nchannels=1, stokes='RR RL LR LL')

# Define the polarization
sm.setfeed('perfect R L', pol=[''] * num_antennas)

# Define the observation parameters
sm.settimes(integrationtime='10s', usehourangle=True, referencetime='2024/01/01/00:00:00')

# Generate the visibilities
sm.observe('TestSource', 'TestSPW', starttime='0h', stoptime='1h')

# Close the simulator
sm.close()

# Plot the simulated data
casatasks.plotms(vis='simulation.ms', xaxis='time', yaxis='amp', correlation='RR,LL')