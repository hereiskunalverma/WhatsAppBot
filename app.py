from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import requests
import time
import os
from google.cloud import dialogflow_v2 as dialogflow
import asyncio
import pytz
from pytz import timezone
from datetime import datetime, date, time
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()
app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mystical-accord-329309-a010cb2b09dd.json"

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "mystical-accord-329309"


def getContest():
    r = requests.get('https://kontests.net/api/v1/all')
    data = r.json()
    contests = []
    for i in data:
        if i['site'] in ['CodeChef', 'CodeForces', 'LeetCode', 'AtCoder']:
            contests.append(i)

    final_contest_list = list()
    flag = 0
    for i in contests:
        flag = 1 if i['site'] == 'CodeChef' else 0
        contest_time = datetime.strptime(
            i['start_time'], '%Y-%m-%d %H:%M:%S %Z') if flag else datetime.strptime(i['start_time'], '%Y-%m-%dT%H:%M:%S.%fz')
        now_time = datetime.now()
        if (contest_time.day >= now_time.day and contest_time.month >= now_time.month and contest_time.year >= now_time.year):
            now_asia = contest_time.astimezone(timezone('Asia/Kolkata'))
            # we need to strip 'Z' before parsing
            d = now_asia if flag else datetime.fromisoformat(
                i['start_time'][:-1]).replace(tzinfo=pytz.utc)
            start_time = d.astimezone(pytz.timezone(
                'Asia/Kolkata')).strftime('%d-%b-%Y %I:%M %p')
            final_contest_list.append(
                {'Name': i['name'], 'Site': i['site'], 'Time': start_time, 'Link': i['url']})
    data = "\tUpcoming Contests\n"
    j = 0
    for j, i in enumerate(final_contest_list):
        if j > 5:
            break
        data += f"\nName: {i['Name']}\nSite: {i['Site']}\nTime: {i['Time']}\nLink: {i['Link']}\n"

    return data, j


def getContest_24():
    r = requests.get('https://kontests.net/api/v1/all')
    data = r.json()
    contests = []
    for i in data:
        if i['site'] in ['CodeChef', 'CodeForces', 'LeetCode', 'AtCoder'] and i["in_24_hours"] == "Yes":
            contests.append(i)

    final_contest_list = list()
    flag = 0
    for i in contests:
        flag = 1 if i['site'] == 'CodeChef' else 0
        contest_time = datetime.strptime(
            i['start_time'], '%Y-%m-%d %H:%M:%S %Z') if flag else datetime.strptime(i['start_time'], '%Y-%m-%dT%H:%M:%S.%fz')
        now_time = datetime.now()
        if (contest_time.day >= now_time.day and contest_time.month >= now_time.month and contest_time.year >= now_time.year):
            now_asia = contest_time.astimezone(timezone('Asia/Kolkata'))
            # we need to strip 'Z' before parsing
            d = now_asia if flag else datetime.fromisoformat(
                i['start_time'][:-1]).replace(tzinfo=pytz.utc)
            start_time = d.astimezone(pytz.timezone(
                'Asia/Kolkata')).strftime('%d-%b-%Y %I:%M %p')
            final_contest_list.append(
                {'Name': i['name'], 'Site': i['site'], 'Time': start_time, 'Link': i['url']})
    data = "\tUpcoming Contests in 24 hours\n"
    for i in final_contest_list:
        data += f"\nName: {i['Name']}\nSite: {i['Site']}\nTime: {i['Time']}\nLink: {i['Link']}\n"

    return data, len(final_contest_list)


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    contests, l = getContest()
    contests_24, l_24 = getContest_24()
    if 'contest' in incoming_msg:
        # return a quote
        if l != 0:
            data = contests
        else:
            data = 'No contest right now'
        msg.body(data)
    elif 'site' in incoming_msg or 'sites' in incoming_msg or 'websites' in incoming_msg or 'website' in incoming_msg:
        sites = ['CodeChef', 'CodeForces', 'LeetCode', 'AtCoder']
        st = ''
        for i in range(len(sites)):
            st += f"\n{i+1}. {sites[i]}"
        msg.body(st)
    elif '24' in incoming_msg:
        if l_24 != 0:
            data = contests_24
        else:
            data = 'No contest in upcoming 24 hours'
        msg.body(data)
    else:
        ans_bot = detect_intent_from_text(incoming_msg, 70141148433)
        msg.body(ans_bot.fulfillment_text)

    return str(resp)


if __name__ == '__main__':
    app.run()
