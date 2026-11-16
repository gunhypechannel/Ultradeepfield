# fb-20261116: "Unable to sign in" (Android, sign-in screen). Auth logs 08:30-08:34 UTC: two sign-ups with empty fields
#   ("Anonymous sign-ins are disabled", "Signup requires a valid password"), two with an address that can't get mail
#   ("Email address ... is invalid"), then a real sign-up that hit Supabase's hourly email limit (429). On a 429 the
#   server does NOT keep the account (no auth.users row), but the game said "Your account is already made" and switched
#   to Sign in, so every later sign-in failed with "Wrong email or password".
# (1) The email-limit message now says no account was made and to try again in about an hour; it no longer flips the
#     form to Sign in. (2) Empty email/password are caught before calling the server. (3) Undeliverable addresses and
#     the anonymous/empty-password errors get plain messages instead of raw server text.
p = 'docs/udf-supabase.js'; t = open(p, encoding='utf-8').read()
R = [
 ('return "We can only send a few emails an hour, so no new one went out. Your account is already made: use the link in the email we sent before (check Spam), or try Resend again in an hour.";',
  'return "Our mail server is busy (it can only send a handful of emails per hour), so nothing was sent. If you were making an account, it wasn\'t made yet: try again in about an hour."; /* fb-20261116: a 429 sign-up keeps no account */'),
 ('if (/invalid format|valid email|Unable to validate email/i.test(m)) return "That email doesn\'t look right.";',
  'if (/invalid format|valid email|Unable to validate email/i.test(m)) return "That email doesn\'t look right.";\n    if (/Email address .* is invalid|email_address_invalid/i.test(m) || (e && e.code === "email_address_invalid")) return "That email address can\'t receive mail. Use your real email."; /* fb-20261116 */\n    if (/Anonymous sign-ins|requires a valid password/i.test(m)) return "Type your email and a password (6+ characters)."; /* fb-20261116 */'),
 ('        if (mode === "reset") return go(sb.auth.resetPasswordForEmail(',
  '        if (!em) return say("Type your email."); /* fb-20261116: an empty form reached the server */\n        if (mode !== "reset" && !pw) return say("Type your password.");\n        if (mode === "up" && pw.length < 6) return say("Use at least 6 characters.");\n        if (mode === "reset") return go(sb.auth.resetPasswordForEmail('),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
