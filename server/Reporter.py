"""
REPORTER

Class responsible for taking the result of the system and
outputting valuable information from the data section
in a pdf
"""
import os
import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import numpy as np
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plot

#
# PATIENT_SCORE = {
#     'name': 'data-1',
#     'ftap':  [0.0, 0.0],
#     'htap':  [0.0, 0.0],
#     'ptrem': [0.0, 0.0],
#     'ktrem': [0.0, 0.0],
#     'rtrem': [0.0, 0.0],
#     'crest': [0.0, 0.0]
# }


class Reporter(object):

    POINT = 1
    INCH = 72
    FILENAME = "score.pdf"
    REPORT = "UPDAReport.pdf"
    GRAPH = "graph.pdf"

    def __init__(self, filepath):
        self.__patient_path = filepath

    def generate_report(self, score):
        """

        :return:
        """
        self.__generate_score(score=score)
        self.__merge_reports(patient_path=self.__patient_path)
        os.remove("{}/{}".format(self.__patient_path, self.FILENAME))
        # self.__generate_graphs()

        # combine header and score with graphs
        # merger = PdfFileMerger()
        # head = open("UPDAReport.pdf", "rb")
        # graph = open("graph.pdf", "rb")
        # merger.append(head)
        # head.close()
        # merger.append(graph)
        # graph.close()

        # output = open("UPDAReport.pdf", "wb")
        # merger.write(output)
        # output.close()
        # remove excess files
        # os.remove("graph.pdf")
        # os.remove("score.pdf")
        print("UPDAReport Complete!")

    def graph_imu(self, fig_num, filename, datasets, titles, xlabel, ylabel):
        # assuming 3 datasets = [x, y, z]
        # titles = [ main , x, y, z]
        # print(len(datasets[0]))
        plot.plot([1,2,3,4])
        plot.show()
        plot.close()

    def __generate_graphs(self):
        """

        :return:
        """
        # generating graph output for the data
        c = canvas.Canvas("{}/{}".format(self.__patient_path, self.GRAPH), pagesize=(8.5 * self.INCH, 11 * self.INCH))
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 18 * self.POINT)
        c.drawString(3 * self.INCH, 10 * self.INCH, "Raw Data Visualization")
        c.setFont("Helvetica", 12 * self.POINT)

        c.showPage()
        c.save()

        # generate images and store them in PDF form
        HAx, HAy, HAz = [], [], []
        HGx, HGy, HGz = [], [], []
        TAx, TAy, TAz = [], [], []
        TGx, TGy, TGz = [], [], []
        PAx, PAy, PAz = [], [], []
        PGx, PGy, PGz = [], [], []
        RAx, RAy, RAz = [], [], []
        RGx, RGy, RGz = [], [], []

        with open("{}/raw.txt".format(self.__patient_path), "r") as file:
            for line in file:
                vals = line.split(sep=' ')
                # HAND
                HAx.append(vals[2])
                HAy.append(vals[3])
                HAz.append(vals[4])
                HGx.append(vals[5])
                HGy.append(vals[6])
                HGz.append(vals[7])
                # THUMB
                TAx.append(vals[11])
                TAy.append(vals[12])
                TAz.append(vals[13])
                TGx.append(vals[14])
                TGy.append(vals[15])
                TGz.append(vals[16])
                # POINT
                PAx.append(vals[20])
                PAy.append(vals[21])
                PAz.append(vals[22])
                PGx.append(vals[23])
                PGy.append(vals[24])
                PGz.append(vals[25])
                # RING
                RAx.append(vals[29])
                RAy.append(vals[30])
                RAz.append(vals[31])
                RGx.append(vals[32])
                RGy.append(vals[33])
                RGz.append(vals[34])

        # create images
        # hand graphing
        self.graph_imu(1, "ha.pdf", [HAx, HAy, HAz], ["Dorsum of Hand Acceleration", "X", "Y", "Z", "XYZ"], "Time (ms)", "Acceleration (g)")
        # self.graph_imu(2, "hg.pdf", [HGx, HGy, HGz], ["Dorsum of Hand Gyroscope", "X", "Y", "Z", "XYZ"], "Time (ms)", "Gyroscope (rads/sec)")
        # thumb graphing
        # self.graph_imu(3, "ta.pdf", [TAx, TAy, TAz], ["Thumb Acceleration", "X", "Y", "Z", "XYZ"], "Time (ms)", "Acceleration (g)")
        # self.graph_imu(4, "tg.pdf", [TGx, TGy, TGz], ["Thumb Gyroscope", "X", "Y", "Z", "XYZ"], "Time (ms)", "Gyroscope (rads/sec)")
        # point graphing
        # self.graph_imu(1, "pa.pdf", [PAx, PAy, PAz], ["Pointer Acceleration", "X", "Y", "Z", "XYZ"], "Time (ms)", "Acceleration (g)")
        # self.graph_imu(2, "pg.pdf", [PGx, PGy, PGz], ["Pointer Gyroscope", "X", "Y", "Z", "XYZ"], "Time (ms)", "Gyroscope (rads/sec)")
        # ring graphing
        # self.graph_imu(1, "ra.pdf", [RAx, RAy, RAz], ["Ring Acceleration", "X", "Y", "Z", "XYZ"], "Time (ms)", "Acceleration (g)")
        # self.graph_imu(2, "rg.pdf", [RGx, RGy, RGz], ["Ring Gyroscope", "X", "Y", "Z", "XYZ"], "Time (ms)", "Gyroscope (rads/sec)")

        # append all images to graph
        # merger = PdfFileMerger()
        # g = open("graph.pdf", "rb")
        # files = ["ha.pdf", "hg.pdf", "ta.pdf", "tg.pdf", "pa.pdf", "pg.pdf", "ra.pdf", "rg.pdf"]
        # merger.append(g)
        # g.close()

        # for f in files:
        #     pic = open(f, "rb")
        #     merger.append(pic)
        #     pic.close()

        # out = open("graph.pdf", "wb")
        # merger.write(out)
        # out.close()
        # remove excess files
        # for f in files:
        #     os.remove(f)


    def __generate_score(self, score):
        """

        :param patient_path:
        ex: ./data/data-1

        :return:
        """

        if not os.path.exists(path=self.__patient_path):
            print("error: {} does not exist, cannot generate report".format(self.__patient_path))
            return

        c = canvas.Canvas("{}/score.pdf".format(self.__patient_path), pagesize=(8.5*self.INCH, 11*self.INCH))
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 12 * self.POINT)

        # generate data name
        v = 10 * self.INCH
        c.drawString(7 * self.INCH, v, score['name'])
        # generate datetime
        v = 10 * self.INCH
        v -= 12 * 4 * self.POINT
        c.drawString(3.25 * self.INCH, v, str(datetime.datetime.now()))
        # generate finger tap scores
        v = 10 * self.INCH
        v -= 12 * 12.5 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['ftap'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['ftap'][1]))
        # generate hand movement scores
        v = 10 * self.INCH
        v -= 12 * 14.75 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['htap'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['htap'][1]))
        # generate postural tremor scores
        v = 10 * self.INCH
        v -= 12 * 17 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['ptrem'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['ptrem'][1]))
        # generate kinetic tremor scores
        v = 10 * self.INCH
        v -= 12 * 19.25 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['ktrem'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['ktrem'][1]))
        # generate rest tremor scores
        v = 10 * self.INCH
        v -= 12 * 21.5 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['rtrem'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['rtrem'][1]))
        # generate consistency of rest scores
        v = 10 * self.INCH
        v -= 12 * 23.75 * self.POINT
        # c.drawString(4.25 * self.INCH, v, "{}%".format(score['crest'][0]))
        c.drawString(6.40 * self.INCH, v, "{}".format(score['crest'][1]))

        c.showPage()
        c.save()

    def __merge_reports(self, patient_path):
        """

        :param patient_path:
        ex: ./data/data-1

        :return:
        """
        output = PdfFileWriter()

        head = PdfFileReader(open("./resources/HeadScore.pdf", "rb"))
        head_page = head.getPage(0)

        score = PdfFileReader(open("{}/{}".format(patient_path, self.FILENAME), "rb"))
        head_page.mergePage(score.getPage(0))

        output.addPage(head_page)
        output_stream = open("{}/{}".format(patient_path, self.REPORT), "wb")
        output.write(output_stream)
