import re 
import os
import time
from JobRecord import JobRecord
import AutoCMSUtil

def build(newWebpageName,config,records):

  yesterday = int(time.time()) - 24 * 3600

  with open(newWebpageName,'w') as webpage:

    AutoCMSUtil.beginWebpage(webpage,config)

    # run and wait time plot (not log scaled)
    plot1name = config['AUTOCMS_TEST_NAME']+"_success24runwait.png"
    plot1path = config['AUTOCMS_WEBDIR']+"/"+plot1name
    AutoCMSUtil.createRunAndWaitTimePlot(plot1path,False,filter(
      lambda job: job.startTime > yesterday \
                  and job.isComplete() \
                  and job.isSuccess() ,
      records.values()
      )
    )
    webpage.write( '<img src="%s">\n' % plot1name )

    webpage.write( '<hr />\n' )

    # description and statistics
    AutoCMSUtil.writeTestDescription(webpage,config)
    webpage.write('<hr />\n')
    AutoCMSUtil.writeBasicJobStatistics(webpage,config,records)
    webpage.write('<hr />\n')

    # start a list of jobs to be printed
    printedJobs = list()

    # print failed jobs from last 24 hours, add them to the list
    webpage.write('<h3>Errors from the last 24 Hours</h3><hr />')
    printedJobs = printedJobs + AutoCMSUtil.writeJobRecords(
      '<b>ERROR</b>',
      webpage,
      config,
      filter( lambda job: job.startTime > yesterday \
                          and job.isComplete() \
                          and not job.isSuccess() ,
              records.values() ),
      inputFile='Input File',
      errorString='Error Type'
    )

    # print successful jobs if requested, add them to the list
    if int(config['AUTOCMS_PRINT_SUCCESS']) == 1:
      webpage.write('<h3>Successful Jobs</h3><hr />' )
      printedJobs = printedJobs + AutoCMSUtil.writeJobRecords(
          'Success',
           webpage,
           config,
           filter( lambda job: job.startTime > yesterday \
                               and job.isComplete() \
                               and job.isSuccess(),
                   records.values() ),
           inputFile='Input File'
      )

    AutoCMSUtil.endWebpage(webpage,config)

    return printedJobs
