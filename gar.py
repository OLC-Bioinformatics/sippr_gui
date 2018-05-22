#!/usr/bin/env/python3
from pylatex.utils import italic, bold
import pylatex
from datetime import datetime
import pandas
import os
__author__ = 'adamkoziol'


class GAR(object):

    def main(self):
        self.file_assertions()
        self.sample_names()
        self.extract_report_data()
        self.create_gar()

    def file_assertions(self):
        """

        """
        for report_name, report_file in self.report_dict.items():
            assert os.path.isfile(report_file), 'No {rn}!'.format(rn=report_name)

    def sample_names(self):
        """
        Extract the sample names from the SampleSheet
        """
        with open(self.sample_sheet) as sample_sheet:
            for line in sample_sheet:
                if 'Sample_ID' in line:
                    for subline in sample_sheet:
                        data = subline.split(',')
                        self.samples.append(data[0])

    def extract_report_data(self):
        """

        """
        for report_name, report_file in self.report_dict.items():
            # Initialise a separate key for each report
            self.report_data[report_name] = dict()
            # Read in the report using pandas - convert it to a dictionary
            dictionary = pandas.read_csv(report_file).set_index('Strain').to_dict()
            # Iterate through the dictionary - each header from the CSV file
            for header in dictionary:
                # Sample is the primary key, and value is the value of the cell for that primary key + header combo
                for sample, value in dictionary[header].items():
                    if value == 'nan':
                        clean_value = '-'
                    elif type(value) is float:
                        clean_value = '-'
                    elif '%' in value:
                        clean_value = '+'
                    else:
                        clean_value = value
                    # Populate the dictionary with the variables
                    try:
                        self.report_data[report_name][sample].update({header: clean_value})
                    except KeyError:
                        self.report_data[report_name][sample] = dict()
                        self.report_data[report_name][sample].update({header: clean_value})

    def create_gar(self):
        """
        Create the genesippr analysis report (GAR) that summarises the
        """
        print('Maketh the report!')
        # Date setup
        date = datetime.today().strftime('%Y-%m-%d')
        year = datetime.today().strftime('%Y')

        # Page setup
        geometry_options = {"tmargin": "2cm",
                            "lmargin": "1.8cm",
                            "rmargin": "1.8cm",
                            "headsep": "1cm"}

        doc = pylatex.Document(page_numbers=False,
                               geometry_options=geometry_options)

        header = self.produce_header_footer()

        doc.preamble.append(header)
        doc.change_document_style("header")

        #
        # DOCUMENT BODY/CREATION
        with doc.create(pylatex.Section('GeneSippr Analysis Report', numbering=False)):
            doc.append('GeneSippr!')

            with doc.create(pylatex.Subsection('GeneSeekr Analysis', numbering=False)) as genesippr_section:
                with doc.create(pylatex.Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                    # Header
                    table.add_hline()
                    table.add_row(self.genesippr_table_columns)
                    for sample_name in self.samples:
                        table_data = [sample_name]
                        for data in self.genesippr_headers:
                            try:
                                print(sample_name, data, self.report_data['genesippr'][sample_name][data])
                                table_data.append(self.report_data['genesippr'][sample_name][data])
                            except KeyError:
                                pass
                        table.add_row(table_data)
            self.create_caption(genesippr_section, 'a', "+ indicates marker presence : "
                                                   "- indicates marker was not detected")

        # Create the PDF
        doc.generate_pdf('{}_{}_{}'
                         .format(os.path.join('/home/adamkoziol/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5'), 'gar', date), clean_tex=False)
        print('{}_{}_{}'.format(os.path.join('/home/adamkoziol/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5'), 'gar', date))
        # for report_name in self.report_data:
        #     for sample_name in self.samples:
        #         for header, value in self.report_data[report_name][sample_name].items():
        #             print(report_name, sample_name, header, value)

    def produce_header_footer(self):
        """
        Adds a generic header/footer to the report. Includes the date and CFIA logo in the header,
        and legend in the footer.
        """
        header = pylatex.PageStyle("header", header_thickness=0.1)

        image_filename = self.get_image()
        with header.create(pylatex.Head("L")) as logo:
            logo.append(pylatex.StandAloneGraphic(image_options="width=110px", filename=image_filename))

        # Date
        with header.create(pylatex.Head("R")):
            header.append("Date Report Issued: " + datetime.today().strftime('%Y-%m-%d'))

        # Footer
        with header.create(pylatex.Foot("C")):
            with header.create(pylatex.Tabular('lcr')) as table:
                table.add_row('', bold('Data interpretation guidelines can be found in RDIMS document ID: 10401305'),
                              '')
                table.add_row('', bold('This report was generated with OLC AutoROGA v0.0.1'), '')
        return header

    @staticmethod
    def get_image():
        """
        :return: full path to image file
        """
        image_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'CFIA_logo.png')
        return image_filename

    @staticmethod
    def create_caption(section, superscript, text):
        """
        Adds a caption preceded by superscripted characters to a table
        :param section: LateX section object
        :param superscript: character(s) to superscript
        :param text: descriptive text
        """
        section.append('\n')

        # Superscript
        section.append(bold(pylatex.NoEscape(r'{\footnotesize \textsuperscript {' + superscript + '}}')))

        # Text
        section.append(italic(pylatex.NoEscape(r'{\footnotesize {' + text + '}}')))


    def __init__(self, inputobject):
        print(inputobject.miseqfolder)
        self.outputfolder = os.path.join(inputobject.outputfolder, inputobject.miseqfolder, 'reports')
        self.miseqfolder = os.path.join(inputobject.miseqfolder)
        self.sample_sheet = inputobject.samplesheet
        self.report_dict = {
            'genesippr': os.path.join(self.outputfolder, 'genesippr.csv'),
            'sixteens_full': os.path.join(self.outputfolder, 'sixteens_full.csv'),
            'GDCS': os.path.join(self.outputfolder, 'GDCS.csv')
        }
        self.report_data = dict()
        self.samples = list()
        self.genesippr_headers = (
            'Strain',
            'Genus',
            'eae',
            'O26',
            'O45',
            'O103',
            'O111',
            'O121',
            'O145',
            'O157',
            'VT1',
            'VT2',
            'VT2f',
            'uidA',
            'hlyA',
            'IGS',
            'inlJ',
            'invA',
            'stn'
        )
        self.genesippr_table_columns = [bold(x) for x in self.genesippr_headers]
        # self.genesippr_table_columns = (
        #     bold('Strain'),
        #     bold('Genus'),
        #     bold('eae'),
        #     bold('O26'),
        #     bold('O45'),
        #     bold('O103'),
        #     bold('O111'),
        #     bold('O121'),
        #     bold('O145'),
        #     bold('O157'),
        #     bold('VT1'),
        #     bold('VT2'),
        #     bold('VT2f'),
        #     bold('uidA'),
        #     bold('hlyA'),
        #     bold('IGS'),
        #     bold('inlJ'),
        #     bold('invA'),
        #     bold('stn')
        # )
        self.main()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    args = parser.parse_args()
    args.miseqpath = '/home/adamkoziol/Bioinformatics/miseq_data'
    args.miseqfolder = '161104_M02466_0002_000000000-AV4G5'
    args.outputfolder = '/home/adamkoziol/Bioinformatics/sippr/gui/'
    args.samplesheet = '/home/adamkoziol/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5/161104_M02466_0002_000000000-AV4G5/full_full/SampleSheet_modified.csv'
    GAR(args)
