class AQI:
    AQI = (
        (0, 50),
        (51, 100),
        (101, 150),
        (151, 200),
        (201, 300),
        (301, 400),
        (401, 500),
    )

    _PM2_5 = (
        (0, 12),
        (12.1, 35.4),
        (35.5, 55.4),
        (55.5, 150.4),
        (150.5, 250.4),
        (250.5, 350.4),
        (350.5, 500.4),
    )

    _PM10_0 = (
        (0, 54),
        (55, 154),
        (155, 254),
        (255, 354),
        (355, 424),
        (425, 504),
        (505, 604),
    )

    @classmethod
    def PM2_5(cls, data):
        return cls._calculate_aqi(cls._PM2_5, data)

    @classmethod
    def PM10_0(cls, data):
        return cls._calculate_aqi(cls._PM10_0, data)

    @classmethod
    def _calculate_aqi(cls, breakpoints, data):
        for index, data_range in enumerate(breakpoints):
            if data <= data_range[1]:
                break

        i_low, i_high = cls.AQI[index]
        C_low, c_high = data_range
        return (i_high - i_low) / (c_high - C_low) * (data - C_low) + i_low

    @classmethod
    def aqi(cls, pm2_5_atm, pm10_0_atm):
        pm2_5 = cls.PM2_5(pm2_5_atm)
        pm10_0 = cls.PM10_0(pm10_0_atm)
        return max(pm2_5, pm10_0)
