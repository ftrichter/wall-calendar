#!/usr/bin/python3

from calendar import Calendar, CalendarError
import sys
import argparse
import cairocffi as cairo#
import os


class FSCalendar(Calendar):
    BLUE = {'red': 75/255, 'green': 101/255, 'blue': 170/255}
    RED = {'red': 241/255, 'green': 73/255, 'blue': 87/255}
    RED_LIGHT = {'red': 250/255, 'green': 201/255, 'blue': 205/255}
    GREEN = {'red': 108/255, 'green': 192/255, 'blue': 41/255}
    GREEN_LIGHT = {'red': 211/255, 'green': 236/255, 'blue': 192/255}
    YELLOW = {'red': 255/255, 'green': 251/255, 'blue': 38/255}
    YELLOW_LIGHT = {'red': 255/255, 'green': 254/255, 'blue': 191/255}

    def __init__(self, year, birthdays, events_small, events_main):
        Calendar.__init__(self, year, "de_DE")

        # colors
        self.add_color(FSCalendar.RED, FSCalendar.RED_LIGHT,
                       FSCalendar.RED, FSCalendar.RED_LIGHT)
        self.add_color(FSCalendar.GREEN, FSCalendar.GREEN_LIGHT,
                       FSCalendar.GREEN, FSCalendar.GREEN_LIGHT)
        self.add_color(FSCalendar.YELLOW, FSCalendar.YELLOW_LIGHT,
                       FSCalendar.YELLOW, FSCalendar.YELLOW_LIGHT)

        # data sources
        if birthdays:
            for f in birthdays:
                self.add_data(f, "top")

        if events_small:
            for f in events_small:
                self.add_data(f, "bottom")

        if events_main:
            for f in events_main:
                self.add_data(f, "main")

    def create(self, filename):
        Calendar.create(self, filename)

        # logo (FIXME)
        #self.print_text("M P I", self.WIDTH-100, 10, 300, FSCalendar.BLUE,
        #                "tr")

        # print year with different bases
        self.print_text(str(self.year), 2000, 50, 200, FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 16), 100, 175, 100,
                        FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 2), 200, 50, 100,
                        FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 8), 800, 175, 100,
                        FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 17), 1000, 50, 100,
                        FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 3), 1150, 175, 100,
                        FSCalendar.BLUE)
        self.print_text(self.__to_base(self.year, 21), 1530, 50, 100,
                        FSCalendar.BLUE)
        
        #check for png and print it on the calendar if present
        if os.path.exists("../wall-calendar/fsmpi_fixed.png"):
             self.print_png(self.load_png("../wall-calendar/fsmpi_fixed.png"))

    def load_png(self, path: str): 
        pngsurface=cairo.ImageSurface.create_from_png(path)
        return pngsurface

    def __to_base(self, number, base):
        if base < 2 or base > 36:
            return None

        div_result = number
        result = ""

        while(div_result != 0):
            digit = div_result % base
            div_result = int(div_result / base)
            result = self.__digit_str(digit) + result

        return result

    def __digit_str(self, digit):
        if digit >= 0 and digit <= 9:
            return str(digit)
        elif digit >= 10 and digit <= 35:
            return chr(65 + digit - 10)

        return None


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int, required=True,
                        help="year of the calendar")
    parser.add_argument("-b", "--birthdays", nargs="+",
                        metavar="file", help="CSV file with birthdays")
    parser.add_argument("-e", "--events", metavar="file",
                        nargs="+",
                        help="CSV file with events, that are printed small")
    parser.add_argument("-m", "--main-events", metavar="file",
                        nargs="+",
                        help="CSV file with main events, that are printed big")
    parser.add_argument("-o", "--output", required=True, metavar="file",
                        help="output file for SVG")
    parser.add_argument("-opdf", "--output-pdf", required=False, metavar="file",
                        help="output file for PDF")
    args = parser.parse_args()

    # run
    try:
        cal = FSCalendar(args.year, args.birthdays, args.events,
                         args.main_events)
        cal.create(args.output)

        if args.output_pdf:
            pdf = cairo.PDFSurface(args.output_pdf, Calendar.WIDTH, Calendar.HEIGHT)
            ctx = cairo.Context(pdf)

            ctx.set_source_surface(cal.surface)
            ctx.paint()

    except CalendarError as e:
        print(str(e))
        sys.exit(1)
