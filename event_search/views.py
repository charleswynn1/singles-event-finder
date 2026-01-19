from django.shortcuts import render
from search_history.models import SearchHistory
from django.contrib.auth.decorators import login_required
#from perplexity import Perplexity
from openai import OpenAI
from decouple import config

openai_client = OpenAI(api_key=config('OPENAI_API_KEY'))
perplexity_client = OpenAI(api_key=config('PERPLEXITY_API_KEY'), base_url="https://api.perplexity.ai")

@login_required
def search_events(request):
    events = []
    if request.method == "POST":
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        user_prompt = f"Where can i meet singles in {city}, {state} between {start_date} and {end_date}? For each event, provide the complete venue address including city and state in the location field. Put the date and time in the date field. Convert time to 12hour format."

        #PerplexityAI Call
        #response = perplexity_client.chat.completions.create(
        #model="sonar-pro",
        #messages=[{"role": "user", "content": user_prompt}],
        #extra_body={
        #"search_recency_filter": "month"
        #}
        #)
        #OpenAI Call
        answer = openai_client.responses.create(
            model="gpt-4.1",
            input=user_prompt,
            tools=[{"type": "web_search_preview"}],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "events_list",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "events": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "date": {"type": "string"},
                                        "location": {"type": "string"},
                                        "cost": {"type": "string"},
                                        "description": {"type": "string"}    
                                    },
                                    "required": ["name", "date", "location", "cost","description"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["events"],
                        "additionalProperties": False
                    }
                }
            }
        )
        import json
        result = json.loads(answer.output_text)
        events = result['events']
        SearchHistory.objects.create(
            user = request.user,
            city = city,
            state = state,
            country = country,
            start_date = start_date,
            end_date = end_date
        )
    return render(request, 'event_search/search.html', {'events': events})
