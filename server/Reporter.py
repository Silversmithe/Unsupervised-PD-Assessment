"""
[CLASS] Reporter

Date:       Tuesday June 12th, 2018
Author:     Alexander Adranly

 Responsible for generating a presentable report for researchers
 and medical professionals. Ideally in the future this can be used
 to effectively diagnose a patients condition
"""
import os
import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas


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

        :param score:
        :return:
        """
        self.__generate_score(score=score)
        self.__merge_reports(patient_path=self.__patient_path)
        os.remove("{}/{}".format(self.__patient_path, self.FILENAME))
        print("UPDAReport Complete!")

    def __generate_score(self, score):
        """
        :param patient_path:
        ex: ./data/data-1
        Generate a PDF with the score of the patient's tremors for the day
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
        Combine scoring PDF with UPDA template to make it look nicer
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
