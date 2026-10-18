"""Service pages: one per product, grouped into the two systems shown on the homepage.

Layout follows the Stone Systems service pages Tim liked (hook line, 4 benefits, demo video,
"What is it?" explainer cards), rewritten for UK domestic plumbers.

House rules (CLAUDE.md): no invented stats or results, no promised rankings or timescales,
no review gating or incentives, "after hours" not "24/7", no prices on these pages.
Add a demo video by setting "video" to its embed URL (e.g. a Loom share link); the section
only shows once a video exists.
"""

GROUPS = {
    1: ("Win more jobs", "Get found on Google and ChatGPT, backed by real reviews, "
                         "and bring past customers back for more."),
    2: ("Stop losing jobs", "Every missed call or unanswered quote is a boiler install for your competition. "
                            "These make sure every enquiry gets a reply."),
}

# Order matters: this is the order on the homepage and the services page.
SERVICE_PAGES = {
    # ---------- 1. Win more jobs ----------
    "websites": {
        "group": 1, "icon": "monitor", "name": "Lead-generating website",
        "title": "Websites for Domestic Plumbers | Vouch Digital",
        "desc": "A fast, mobile-friendly website that turns visitors into text conversations on your phone. "
                "Free with the plan, live in 3–5 days. For domestic plumbers across the UK.",
        "h1": "A website that <span class=\"accent\">turns visitors into enquiries.</span>",
        "lede": "Not just a pretty brochure. Every enquiry from your website turns into a text conversation that goes "
                "straight to your phone. Free with the plan, and live in 3–5 days.",
        "tagline": "A customer googles your business and can't find you? Awkward. Let's not let that happen.",
        "benefits": [
            ("Actually get found online",
             "Built properly for Google from day one: the right page titles, headings and a page for each service."),
            ("Show off your real reviews",
             "Your genuine Google reviews on your site, updating automatically as new ones come in."),
            ("Looks great on a phone",
             "Most customers will look at your site on their phone, often in a hurry. We design for that first."),
            ("Enquiries straight to your phone",
             "Forms and a chat box that start a text conversation, so you can reply from the van."),
        ],
        "explain_h2": "What you get with your website",
        "explain": [
            ("search", "Built for local searches",
             "A clear page for each service you offer and the areas you cover, set up the way Google likes, "
             "and quick to load."),
            ("star", "Your Google reviews, live",
             "Your real reviews pulled straight from Google and kept up to date. Never made-up testimonials."),
            ("monitor", "Mobile-first design",
             "Your number and a call button always in reach, big buttons, and nothing that's fiddly on a small screen."),
            ("mail", "Instant text conversations",
             "Quote forms and a chat widget that text the customer straight back, so you have their number even if "
             "they leave your site."),
        ],
        "split": (["Fill in a short onboarding form", "Send photos of your work",
                   "Check the draft and tell us what to change"],
                  ["Write the words", "Design and build the site",
                   "Set up hosting and your domain", "Keep it updated as your business changes"]),
        "faq": [
            ("Is the website really free?",
             "Yes, when you're on the monthly plan it's included at no extra cost. If you only want a website on its "
             "own, it's £1,499 as a one-off."),
            ("I already have a website. Do I need a new one?",
             "Not always. If your site works well, we can work with it. If it's slow, hard to use on a phone or not "
             "bringing in enquiries, a new one will do a better job. We'll tell you honestly on the call."),
            ("Do I own my domain?",
             "Yes. Your domain is registered in your business's name, not ours."),
            ("How long does it take?",
             "Usually 3–5 days once we have your onboarding form and photos."),
        ],
    },
    "google-reviews": {
        "group": 1, "icon": "star", "name": "Genuine Google reviews",
        "title": "Google Reviews for Domestic Plumbers | Vouch Digital",
        "desc": "Every customer asked for a genuine Google review by text and email, with polite reminders and a reply "
                "to every review. Fully compliant. For domestic plumbers across the UK.",
        "h1": "Turn happy customers into <span class=\"accent\">genuine Google reviews.</span>",
        "lede": "“Sure, I'll leave you a review!” Then they forget. We ask every customer at the right moment, "
                "remind them politely, and reply to every review for you. Real reviews only.",
        "tagline": "“Sure, I'll leave you a review.” The truth is, people forget. We gently remind them.",
        "benefits": [
            ("Every customer asked",
             "A friendly text and email after every job, with a direct link to your Google review page."),
            ("Polite reminders",
             "Busy people forget. A couple of spaced-out reminders, then we stop. No nagging."),
            ("Ask in one click",
             "Finished a job? Pop the customer's name and number into the app and the system does the rest."),
            ("Real reviews, done properly",
             "We never filter out unhappy customers, buy reviews or offer rewards. That's the law, and it's how "
             "reviews keep their value."),
        ],
        "explain_h2": "How we get you more genuine reviews",
        "explain": [
            ("mail", "Review requests by text and email",
             "Sent after each job, worded for plumbing and signed off as your business, with a one-tap link to Google."),
            ("clock", "Automatic follow-up reminders",
             "If they haven't left one, a reminder goes out a few days later, then another. It stops as soon as they "
             "review or ask us to stop."),
            ("user", "Past customers too",
             "A one-off campaign to customers from the last couple of years, where you're allowed to contact them."),
            ("star", "A reply to every review",
             "Thoughtful replies that mention the job and the area, and calm, professional replies to any bad ones."),
        ],
        "split": (["Add customers in the app after each job (or connect your job software)",
                   "Do great work, like you already do"],
                  ["Write and send every review request", "Chase politely, then stop",
                   "Reply to every review", "Keep it all compliant with UK law"]),
        "faq": [
            ("Are the reviews genuine?",
             "Yes. We only ask your real customers. "
             "We never write, buy, incentivise or remove reviews. That's what the Digital Markets, Competition and "
             "Consumers Act 2024 requires."),
            ("What if someone leaves a bad review?",
             "It happens to every business. We'll write a calm, professional reply for you to approve. A good reply to "
             "a bad review often reassures future customers more than another five stars."),
            ("Can you get my customer list from my job software?",
             "Often, yes. Tools like Tradify, ServiceM8, Jobber and Powered Now can usually be connected. If not, "
             "a simple spreadsheet works fine."),
        ],
    },
    "google-business-profile": {
        "group": 1, "icon": "pin", "name": "Google profile, local SEO & AI search",
        "title": "Google Business Profile & Local SEO for Plumbers | Vouch Digital",
        "desc": "Your Google Business Profile, local listings and website kept complete and active, so you can show up "
                "for “plumber near me” in Google and ChatGPT. For domestic plumbers across the UK.",
        "h1": "Show up when locals search <span class=\"accent\">“plumber near me”.</span>",
        "lede": "Your Google profile is often the first thing a customer sees. We set it up properly, keep it active, "
                "and tidy up everything else online that Google and ChatGPT look at before they recommend a plumber.",
        "tagline": "“Number one on Google in a week!” Just kidding. It takes time, and we do the work every month.",
        "benefits": [
            ("Found on Google Maps",
             "Every section of your profile filled in properly: services, areas, categories and photos."),
            ("Visible in ChatGPT too",
             "AI tools read your reviews, listings and website. We make sure they all tell the same clear story."),
            ("Stop paying for tyre-kickers",
             "Customers who find you themselves already want you. No paying per lead for people who never pick up."),
            ("Done every month",
             "Posts, photos and fixes added regularly, so your profile stays active instead of going stale."),
        ],
        "explain_h2": "What we look after for you",
        "explain": [
            ("pin", "Google Business Profile",
             "The right categories and service areas, every service listed, your real job photos, and regular posts "
             "about recent work."),
            ("link", "Listings across the web",
             "Your name, number and services made consistent on Bing, Apple Maps, Yell and trade directories."),
            ("search", "Local SEO on your website",
             "Pages for your main services and areas, and the behind-the-scenes details that help search engines "
             "read your site."),
            ("ai", "AI search checks",
             "We ask ChatGPT and Google's AI answers who they recommend in your area, and keep improving what they "
             "can read about you."),
        ],
        "split": (["Add us as a manager on your Google profile (two minutes, we'll show you)",
                   "Send us photos from your jobs when you can"],
                  ["Fill in every section properly", "Post updates and photos regularly",
                   "Clean up your listings across the web", "Check what Google and ChatGPT say about you"]),
        "faq": [
            ("Will this get me to the top of Google Maps?",
             "We can't promise rankings, and anyone who does is guessing. What we can do is fix the things that hold "
             "profiles back and keep yours complete and active, month after month."),
            ("Can you guarantee ChatGPT will recommend me?",
             "No, and be wary of anyone who says they can. We improve the information these tools rely on, which gives "
             "you the best chance of being mentioned."),
            ("Do I lose control of my Google profile?",
             "No. You stay the owner. We're added as a manager, which you can remove at any time."),
            ("I work from home. Can I still show on Google Maps?",
             "Yes. Most plumbers are set up as a “service-area business”, which hides your home address and "
             "shows the areas you cover instead."),
        ],
    },
    "marketing-campaigns": {
        "group": 1, "icon": "target", "name": "Marketing campaigns",
        "title": "Marketing Campaigns for Plumbers | Vouch Digital",
        "desc": "Automatic boiler service reminders, seasonal offers and referral campaigns to your past customers. "
                "Repeat work from people who already trust you. For domestic plumbers across the UK.",
        "h1": "Win more work from customers <span class=\"accent\">who already trust you.</span>",
        "lede": "Your past customers already like you. Automatic campaigns remind them when their boiler service is due, "
                "send seasonal offers, and nudge them to recommend you to friends and neighbours.",
        "tagline": "You know it, we know it: repeat customers and referrals are the best jobs. Let's get you both.",
        "benefits": [
            ("Done for you",
             "Ready-made campaigns written for plumbers. Pick one in the app and press send."),
            ("Boiler service reminders",
             "Customers reminded every year when their service is due, so the work comes back to you."),
            ("Referrals without the awkward ask",
             "Happy customers gently reminded to recommend you to friends, family and neighbours."),
            ("Fill quiet weeks",
             "Summer slow? Send a seasonal offer to past customers in one click when you want more work."),
        ],
        "explain_h2": "Campaigns ready to go",
        "explain": [
            ("flame", "Annual boiler service reminders",
             "Sent automatically a year after each service or install, with an easy way to book in."),
            ("user", "Referral campaigns",
             "A friendly message to happy customers asking them to pass your name on to anyone who needs a plumber."),
            ("clock", "Seasonal offers",
             "Winter boiler checks, pre-summer bathroom refits, landlord safety checks. Ready to send when you are."),
            ("mail", "Old enquiry revival",
             "A polite check-in with people who asked for a quote but never went ahead, in case they still need you."),
        ],
        "split": (["Pick a campaign when you want more work", "Answer the replies that come in"],
                  ["Write every campaign with you", "Load your past customers in (where you're allowed to contact them)",
                   "Set up the annual service reminders", "Check everything follows UK marketing rules"]),
        "faq": [
            ("Am I allowed to text my old customers?",
             "Usually yes, if they're past customers who were given the chance to opt out and haven't. Every message "
             "includes an easy way to stop. We check this with you before anything is sent."),
            ("Do I have to use the campaigns?",
             "No. The service reminders run on their own, and the other campaigns are there when you want more work. "
             "You decide when to press send."),
            ("How many past customers do I need?",
             "There's no minimum. Even a few dozen past customers is enough to make a campaign worthwhile."),
        ],
    },
    # ---------- 2. Stop losing jobs ----------
    "missed-call-text-back": {
        "group": 2, "icon": "phone", "name": "Missed-call text-back",
        "title": "Missed-Call Text-Back for Plumbers | Vouch Digital",
        "desc": "When you can't answer, the caller gets an instant text from your business so the job doesn't go to "
                "the next plumber. For domestic plumbers across the UK.",
        "h1": "Under a boiler and can't pick up? <span class=\"accent\">We'll text them back for you.</span>",
        "lede": "Everyone misses calls. Not everyone texts back. When you can't answer, the caller gets a friendly text "
                "from your business within seconds, so they wait for you instead of ringing the next plumber.",
        "tagline": "Everyone misses calls, but not everyone texts back. Be the one who does.",
        "benefits": [
            ("Stand out from other plumbers",
             "Most plumbers ring back hours later, if at all. An instant text puts you first in the queue."),
            ("No more lost leads",
             "Hands full on a job? The text goes out automatically and starts the conversation for you."),
            ("Show customers you care",
             "A burst pipe is stressful. A quick “got your call, I’ll be in touch” calms people down."),
            ("Covers after hours too",
             "Missed a call at 9pm? They still get a text, so the enquiry is waiting for you in the morning."),
        ],
        "explain_h2": "How missed-call text-back works",
        "explain": [
            ("phone", "Someone rings and you can't answer",
             "On a job, driving, or just off for the day. The call goes unanswered, like it always would."),
            ("mail", "They get a text from your business",
             "Within seconds, written in your words: who you are, that you'll be in touch, and a link to send "
             "details or photos of the problem."),
            ("clock", "The conversation is waiting for you",
             "Their reply lands in your inbox app with their number, so you can pick it up the moment you're free."),
            ("chart", "You see every missed call",
             "No more guessing who rang. Every missed call is logged, so nothing slips through the cracks."),
        ],
        "split": (["Use your business number on your van, website and Google profile",
                   "Reply when you're free"],
                  ["Set up your business number", "Write the text-back message with you",
                   "Connect it to your inbox app", "Tweak it whenever you want"]),
        "faq": [
            ("Do I need a new phone number?",
             "We set you up with a business number that forwards to your mobile. That's what makes the text-back "
             "possible, and it keeps work and personal calls separate."),
            ("Can I still answer calls normally?",
             "Yes. Calls ring your mobile as usual. The text only goes out when you don't pick up."),
            ("What does the text say?",
             "Whatever suits you. We'll write it with you, in plain English, signed off as your business."),
        ],
    },
    "lead-follow-up": {
        "group": 2, "icon": "clock", "name": "Automated lead follow-up",
        "title": "Automated Lead Follow-Up for Plumbers | Vouch Digital",
        "desc": "Every enquiry gets an instant reply and every quote is chased automatically, so fewer jobs slip away. "
                "For domestic plumbers across the UK.",
        "h1": "Every enquiry answered. <span class=\"accent\">Every quote chased.</span>",
        "lede": "Most quotes aren't lost to a cheaper plumber. They're lost because nobody followed up. We reply to every "
                "enquiry instantly and chase your quotes politely, so you don't have to.",
        "tagline": "Sent a quote and heard nothing? You're not alone. Let the system do the chasing.",
        "benefits": [
            ("Every enquiry answered instantly",
             "Website form, chat or Facebook message: they get a text straight away saying you've got it."),
            ("Quotes chased automatically",
             "A friendly nudge a few days after you quote, then another. You stop chasing, the system does it."),
            ("Stops the moment they reply",
             "No awkward double messages. As soon as the customer gets back to you, the follow-ups stop."),
            ("Sounds like you, not a robot",
             "Short, friendly messages written in your words and signed off as your business."),
        ],
        "explain_h2": "What's in the follow-up system",
        "explain": [
            ("monitor", "Website and chat enquiries",
             "When someone fills in your form or chat, they get an instant text to confirm, and you get a notification "
             "so you can reply properly."),
            ("clipboard", "Quote follow-ups",
             "Sent a quote and heard nothing? A short series of polite texts and emails follows it up, and stops as "
             "soon as they reply."),
            ("mail", "Facebook and Instagram replies",
             "Message you on Facebook or Instagram and they get a quick reply saying you'll be in touch soon."),
            ("chart", "Nothing left hanging",
             "Every open enquiry and quote is tracked in the app, so you can see at a glance who still needs an answer."),
        ],
        "split": (["Mark a quote as sent in the app", "Reply when customers get back to you"],
                  ["Write the follow-up messages with you", "Set up the instant replies",
                   "Connect your website, Facebook and Instagram", "Tweak the timings whenever you want"]),
        "faq": [
            ("Won't customers find it annoying?",
             "The messages are short, spaced out and written like you'd write them. Follow-ups stop the moment someone "
             "replies."),
            ("How many follow-ups are sent?",
             "Usually two or three, spread over a couple of weeks. We'll agree the timing with you."),
            ("Can I turn it off for a customer?",
             "Yes. One tap in the app stops the follow-ups for anyone."),
        ],
    },
    "all-in-one-inbox": {
        "group": 2, "icon": "mail", "name": "All-in-one inbox & business phone",
        "title": "All-in-One Inbox & Business Phone for Plumbers | Vouch Digital",
        "desc": "Calls, texts, emails, Facebook and Instagram messages in one app, on a separate business number. "
                "For domestic plumbers across the UK.",
        "h1": "Every enquiry in one app. <span class=\"accent\">Work and personal kept separate.</span>",
        "lede": "Texts on your phone, emails on the laptop, Facebook messages you forgot to check. We put every enquiry "
                "into one simple app, on a business number that's separate from your personal one.",
        "tagline": "Five apps to check after a long day? Make it one.",
        "benefits": [
            ("One place for everything",
             "Texts, emails, calls, Facebook and Instagram messages, all in one list on your phone."),
            ("Save time every day",
             "No more jumping between apps or scrolling back to find what someone asked for."),
            ("A proper business number",
             "Customers ring your business, not your personal mobile. Switch it off at the weekend if you like."),
            ("Nothing gets forgotten",
             "Every conversation stays with the customer's details, so you can pick it up months later."),
        ],
        "explain_h2": "What's in the inbox",
        "explain": [
            ("mail", "4-in-1 unified inbox",
             "Texts, emails, Facebook messages and Instagram DMs land in one inbox, and you can reply to all of them "
             "from the same place."),
            ("phone", "Business phone number",
             "A local or mobile business number that rings through to your phone, with your name shown to customers."),
            ("chart", "Call history",
             "See who called, when, and whether you answered. Handy for knowing which enquiries came from where."),
            ("user", "Customer details in one place",
             "Name, number, address and every message you've swapped, all saved against the customer."),
        ],
        "split": (["Download the app on your phone", "Reply to customers from one place"],
                  ["Set up your business number", "Connect your email, Facebook and Instagram",
                   "Show you round the app on the launch call", "Help whenever you get stuck"]),
        "faq": [
            ("Can I keep my existing number?",
             "Often, yes. Many numbers can be moved across. If not, we'll set up a new business number and you can "
             "forward your old one to it."),
            ("Does it work on my phone?",
             "Yes. There's an app for iPhone and Android, and it works on a laptop too."),
            ("Do my staff get access?",
             "If you have someone who handles enquiries, they can have their own login."),
        ],
    },

}

for _s in SERVICE_PAGES.values():
    _s.setdefault("video", None)
