import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import human as hm
import robot as rb
import config as cfg


class TrustTransition:
    def __init__(self) -> None:
        # Memory for trust history
        self.cumulative_error_history = [] # recording all the errors in a session
        self.cumulative_trust_history = []
