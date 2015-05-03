# encoding: utf-8
import math
import datetime
import time
# #utf8 info needd to display kanji characters.
#Creating a generic sun object that can calculate sunrise and sunset times
#For specific locations
#Concept for calculating sunrise and sunset from "Calulating sunrise and sunset in Python" by Michele Anders
#Reprogrammed from algorithm by NOAA, "NOAA_Solar_Calculations_year.xls"
#Accessed from http://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html



class Sun(object):
    temperature = "very hot"
    def __init__(self, lattitude, longitude, utc_displacement):
        self.lattitude = lattitude
        self.longitude = longitude
        self.utc_displacement = utc_displacement
    def jday(self):
        #this is based on the algorithm from wikipedia.
        #Calculates the julianday
        w = datetime.datetime.utcnow() #makes a a utc object
        a = math.floor((14-w.month)/12) # calculates variable a
        y = w.year+4800-a
        m = w.month + 12*a - 3
        jdn = w.day + math.floor((153*m+2)/5) + 365*y + math.floor(y/4) - math.floor(y/100) + math.floor(y/400) - 32045
        # the above is the wikipedia algorithm for julian day
        #It assumes it's already noon UTC though. I added the code below to make
        # it exact.
        # It adjusts back (0.5 days) since the julian day started at noon GMT
        # It then converts the hours, minutes and seconds since midnight into
        # the equivalent number of days to give an accurate Julian time
        jdn = jdn - 0.5 + w.hour/24 + w.minute/(24*60) + w.second/(24*60*60)
        return jdn
    def sunrise(self, jd):
        #jd is the julian day
        #There are a number of complicated calculations that followw. A good explanation of the astronomical terms use
        #is available through noaa.gov
        jcent = (jd - 2451545)/36525 #julian century - defined as starting January 1st 2000
        gmls = (280.46646+jcent*(36000.76983 + jcent*0.0003032))%360
        #calculating "Geometric Mean Long Sun (deg)"
        gmas = 357.52911+jcent*(35999.05029 - 0.0001537*jcent)
        #"Geometric Mean Anom Sun (deg)"
        eeo = 0.016708634-jcent*(0.000042037+0.0000001267*jcent)
        #Eccent Earth Orbit
        sun_eqn_ctr = math.sin(math.radians(gmas))*(1.914602-jcent*(0.004817+0.000014*jcent))+math.sin(math.radians(2*gmas))*(0.019993-0.00101*jcent)+math.sin(math.radians(3*gmas))*0.000289
        #Sun Eq of Ctr
        sun_true_long = gmls + sun_eqn_ctr
        #Sun True Long (degrees)
        sun_true_anom = gmas + sun_eqn_ctr
        #Sun True Anom (degrees)
        sun_rad_vector = (1.000001018*(1-eeo**2))/(1+eeo*math.cos(math.radians(sun_true_anom)))
        #Sun Rad Vector (AUs)
        sun_app_long = sun_true_long - 0.00569-0.00478*math.sin(math.radians(125.04-1934.136*jcent))
        #Sun App Long (degrees)
        moe = 23 + (26 + ((21.448-jcent*(46.815+jcent*(0.00059-jcent*0.001813))))/60)/60
        #mean obliq ecliptic (deg)
        obliq_corr = moe + 0.00256*math.cos(math.radians(125.04-1934.136*jcent))
        #obliq corr (degrees)
        sun_rt_ascen = math.degrees(math.atan2(math.cos(math.radians(obliq_corr))*math.sin(math.radians(sun_app_long)),math.cos(math.radians(sun_app_long))))
        #sun rt ascen (deg) - this was complicated. See documentation.
        #ms xcel notation is atan2(x,y)
        #but python math is atan2(y,x) - subtle. Got this wrong the first time
        sun_declin = math.degrees(math.asin(math.sin(math.radians(obliq_corr))*math.sin(math.radians(sun_app_long))))
        #sun declin (deg)
        var_y = math.tan(math.radians(obliq_corr/2))*math.tan(math.radians(obliq_corr/2))
        #var_y (this is just the tangent function squared, but I'm copying the notation
        # of the spreadsheet for consistency
        eqn_of_time = 4*math.degrees(var_y*math.sin(2*math.radians(gmls))-2*eeo*math.sin(math.radians(gmas))+4*eeo*var_y*math.sin(math.radians(gmas))*math.cos(2*math.radians(gmls))-0.5*(var_y**2)*math.sin(4*math.radians(gmls))-1.25*(eeo**2)*math.sin(2*math.radians(gmas)))
        #eqn of time (minutes)
        ha_sunrise = math.degrees(math.acos(math.cos(math.radians(90.833))/(math.cos(math.radians(self.lattitude))*math.cos(math.radians(sun_declin)))-math.tan(math.radians(self.lattitude))*math.tan(math.radians(sun_declin))))
        #ha sunrise (deg)
        solar_noon = (720 - 4*self.longitude - eqn_of_time + self.utc_displacement*60)/1440
        #solar noon (LST) - calculated for local time by taking into account UTC
        #displacement.
        sunrise_time = (solar_noon*1440 - ha_sunrise*4)/1440
        #sunrise time (LST)
        sunset_time = (solar_noon*1440 + ha_sunrise*4)/1440
        #sunset time (LST)
        sunlight_duration = 8*ha_sunrise
        #sunlight duration
        return [solar_noon, sunrise_time, sunset_time, sunlight_duration]
    def wadokei(self):
        jd = self.jday()
        sun_array = self.sunrise(jd) #saves sunrise info in an array
        sun_array_tmrw = self.sunrise(jd+1) #creates a sunrise info array for 12 hours ahead
        sun_array_yest = self.sunrise(jd-1) #sunrise info array for 12 hours before
        #my guess is that this doesn't need to be exact since it changes by only a few minutes per day
        utc_time = datetime.datetime.utcnow() #makes a a utc object for current time
        dec_time = ((utc_time.hour+self.utc_displacement)%24)/24 + utc_time.minute/(24*60) + utc_time.second/(24*3600) #calcs the
        #decimal time for the day, adjusting for utc offset
        if dec_time < 0: #to take care of instances where calculation is negative
            dec_time += 1
        #next I figure out if it's day or night currently
        if sun_array[1] < dec_time and dec_time < sun_array[2]:
            light_status="day"
        else:
            light_status="night"
        #Now I will calculate what part of the day or night it is and turn that into a number from 0 to 6
        if light_status == "day":
            watime = ((dec_time - sun_array[1])*6)/(sun_array[2]-sun_array[1]) #calculates the decimal time since sunset, then divides this by
            #the total sunlight duration (sunset-sunrise time) to get the fraction of sunlight duration that has passed. This is multiplied
            #by 6 to get the wadokei time
        if light_status =="night":
            if (0.600 < dec_time) and (dec_time <= 1):
                watime = 6 + (dec_time - sun_array[2])*6/((1-sun_array[2])+sun_array_tmrw[1]) #have to calculate total night time based on tmrws sunrise. Again
                #again calculating the portion of the night that has passed. Now adding 6 to it to account for daylight hours
            elif (0<dec_time) and (dec_time < 0.400):
                watime = 6 + (dec_time + (1-sun_array_yest[2]))*6/((1-sun_array_yest[2])+sun_array[1]) #numerator is decimal time since sunset. Denominator
                #is total length of the night in decimal time (24 hours = 1.000). 6 hours is added since the 6 daylight hours have gone by
            else:
                watime = "error"
        return [watime, light_status]
    def wadokeihour(self):
        t_array = self.wadokei() #gets the output time array from the wadokei function
        hour = t_array[0]
        windex = math.floor(hour) #floor function so it can be used as an index
        zodiac = ["卯","辰","巳","午","未","申","酉","戌","亥","子","丑","寅"]
        # a list of the zodiac symbols for each hour of the japanese clock
        #the list  index happens to correspond to the hour system I set up
        english = ["rabbit", "dragon", "snake", "horse", "goat", "monkey", "rooster", "dog", "pig", "rat", "ox", "tiger"];
        #english names for each zodiac symbol
        jhour = [6,5,4,9,8,7,6,5,4,9,8,7];
        print("The current hour is " + zodiac[windex] + " - " + english[windex] + ", " + str(jhour[windex]-(hour%1)))
        
