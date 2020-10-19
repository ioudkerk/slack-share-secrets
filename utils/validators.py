import hmac
import hashlib

def verify(request,secret):
    body = request.get_data()
    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_basestring = 'v0:%s:%s' % (timestamp, body.decode('utf-8'))
    computed_sha = hmac.new(secret,
                            sig_basestring.encode('utf-8'),
                            digestmod=hashlib.sha256).hexdigest()
    my_sig = 'v0=%s' % (computed_sha,)
    slack_sig = request.headers['X-Slack-Signature']
    if my_sig != slack_sig:
        err_str = "my_sig %s does not equal slack_sig %s" % (my_sig, slack_sig)
        raise Exception(err_str)
