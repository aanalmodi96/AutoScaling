from flask import Flask, render_template, request, url_for
import json, datetime, random
import time
from awsdb import connect
from awsredis import r


application = Flask(__name__)


# default
@application.route('/', methods=["GET"])
def hello_world():
    # return render_template('index.html', result=obj)
    return render_template('index.html')

@application.route('/photo', methods=["GET"])
def problem_6():
        recd = datetime.datetime.now()
        start = recd.timestamp()

        time = int(recd.strftime('%S'))
        image = ''
        if time % 10 == 0:
            image = url_for('static', filename='a.jpg')
        else:
            image = url_for('static', filename='b.jpg')

        resp = datetime.datetime.now()
        end = resp.timestamp()

        elapsed = (resp.timestamp() - recd.timestamp())

        return render_template('prob6.html', image=image, start=str(start), end=str(end), elapsed=elapsed)


@application.route('/prob1', methods=["POST"])
def problem_1():
    query_count = int(request.form["query_count"])
    use_cache = (request.form["use_cache"] == "True")

    total_time = 0

    for i in range(query_count):

        if (use_cache):
            # cache
            if r.exists("all"):
                # start time
                start_time = datetime.datetime.now().timestamp()

                result = json.loads(r.get("all"))

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
            else:

                # start time
                start_time = datetime.datetime.now().timestamp()

                sql = "SELECT place from quakes"
                cursor = connect.cursor()
                cursor.execute(sql)
                output = cursor.fetchall()

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

                result = []
                for row in output:
                    result.append(row[0])

                r.set("all", json.dumps(result))

        else:
            # no cache

            # start time
            start_time = datetime.datetime.now().timestamp()

            cursor = connect.cursor()
            sql = "SELECT place from quakes"
            cursor.execute(sql)
            output = cursor.fetchall()

            # end time
            total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

            result = []
            for row in output:
                result.append(row[0])

    total_time = total_time * 1000
    return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


@application.route('/prob2', methods=["POST"])
def problem_2():
    start_magnitude = int(request.form["start_magnitude"])
    end_magnitude = int(request.form["end_magnitude"])

    query_count = int(request.form["query_count"])
    use_cache = (request.form["use_cache"] == "True")

    total_time = 0

    for i in range(query_count):
        magnitude = round(random.uniform(start_magnitude, end_magnitude), 1)

        if (use_cache):
            # cache
            if r.exists("mag=" + str(magnitude)):
                # start time
                start_time = datetime.datetime.now().timestamp()

                result = json.loads(r.get("mag=" + str(magnitude)))

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
            else:

                # start time
                start_time = datetime.datetime.now().timestamp()

                sql = "SELECT place from quakes where mag = '" + str(magnitude) + "';"
                cursor = connect.cursor()
                cursor.execute(sql)
                output = cursor.fetchall()

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

                result = []
                for row in output:
                    result.append(row[0])

                r.set("mag=" + str(magnitude), json.dumps(result))

        else:
            # no cache

            # start time
            start_time = datetime.datetime.now().timestamp()

            cursor = connect.cursor()
            sql = "SELECT place from quakes where mag = '" + str(magnitude) + "';"
            cursor.execute(sql)
            output = cursor.fetchall()

            # end time
            total_time + (datetime.datetime.now().timestamp() - start_time)

            result = []
            for row in output:
                result.append(row[0])

    total_time = total_time * 1000
    return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)

# @application.route('/prob6', methods=["POST"])
# def problem_6():
#         start_magnitude = float(request.form["start_magnitude"])
#         end_magnitude = float(request.form["end_magnitude"])
#         query_count = int(request.form["query_count"])
#         use_cache = (request.form["use_cache"] == "True")
#
#         total_time = 0
#
#
#         if (start_magnitude > end_magnitude):
#             return "start magnitude greater than end magnitude"
#
#         mag = start_magnitude
#         ret = {}
#         while mag < end_magnitude:
#
#             lst = connect.mag_in_ranges(mag, mag + 0.1)
#             ret["Magnitude " + str(mag) + " to " + str(mag + 0.1) + ", " + str(len(lst)) + " earthquakes"] = lst
#             mag = mag + 0.1
#
#         return render_template('prob6.html', result=ret)

@application.route('/prob3', methods=["GET"])
def prob():
    number = int(request.form["number"])
    if (number/2==0):
        image = url_for('static', filename='twitter.png')

@application.route('/prob3', methods=["POST"])
def problem_3():
    start_magnitude = int(request.form["start_magnitude"])
    end_magnitude = int(request.form["end_magnitude"])

    query_count = int(request.form["query_count"])
    use_cache = (request.form["use_cache"] == "True")

    total_time = 0

    for i in range(query_count):
        magnitude = round(random.uniform(start_magnitude, end_magnitude), 1)

        if (use_cache):
            # cache
            if r.exists("mag=" + str(magnitude)):
                # start time
                start_time = datetime.datetime.now().timestamp()

                result = json.loads(r.get("mag=" + str(magnitude)))

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
            else:

                # start time
                start_time = datetime.datetime.now().timestamp()

                sql = "SELECT place from quakes where mag = '" + str(magnitude) + "';"
                cursor = connect.cursor()
                cursor.execute(sql)
                output = cursor.fetchall()

                # end time
                total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

                result = []
                for row in output:
                    result.append(row[0])

                r.set("mag=" + str(magnitude), json.dumps(result))

        else:
            # no cache

            # start time
            start_time = datetime.datetime.now().timestamp()

            cursor = connect.cursor()
            sql = "SELECT * from quakes where mag between '" + str(start_magnitude) + "' AND '" + str(end_magnitude) + "';"
            cursor.execute(sql)
            output = cursor.fetchall()

            # end time
            total_time + (datetime.datetime.now().timestamp() - start_time)

            result = []
            for row in output:
                result.append(row[0])

    total_time = total_time * 1000
    return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


if __name__ == '__main__':
    application.debug = True
    application.run()