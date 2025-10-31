# Troubleshooting Guide

## Wikipedia API 403 Forbidden Error

### Problem Description

When running the application, you may encounter the following error:

```
ERROR: Error retrieving Wikipedia data: 403 Client Error: Forbidden for url: https://en.wikipedia.org/w/api.php?action=query&format=json&titles=...
```

### Root Cause

**Wikipedia API requires proper User-Agent identification**

According to [Wikimedia User-Agent Policy](https://meta.wikimedia.org/wiki/User-Agent_policy):
- All automated clients accessing Wikipedia APIs must identify themselves with a User-Agent header
- The User-Agent should include:
  - Application name and version
  - Contact information (URL or email)
- Requests without proper User-Agent headers receive 403 Forbidden responses

### Why It Happened

The original implementation used Python's `requests` library without setting User-Agent headers:

```python
# Original code - No User-Agent
response = requests.get(
    self.WIKIPEDIA_API_URL, 
    params=params,
    timeout=10
)
```

### Solutions

#### Solution 1: Updated Default Implementation (Recommended)

The `src/wikipedia_client.py` has been updated to include proper User-Agent headers:

```python
headers = {
    "User-Agent": "BundesligaCoachRAGChatbot/1.0 (https://github.com/user/bundesliga-coach-rag-chatbot; contact@example.com)"
}

response = requests.get(
    self.WIKIPEDIA_API_URL, 
    params=params,
    headers=headers,
    timeout=10
)
```

**Action Required**: 
- No additional installation needed
- The fix is already applied in the updated code
- For production use, replace the placeholder contact information with your actual project details

#### Solution 2: Use wikipedia-api Library

An alternative implementation using the `wikipedia-api` package is provided in `src/wikipedia_client_alternative.py`.

**Advantages**:
- Handles User-Agent requirements automatically
- More robust error handling
- Cleaner API interface
- Better maintained by the community

**Installation**:
```bash
pip install wikipedia-api
```

**Usage**:
Modify `main.py` line 13:
```python
# Change from:
from src.wikipedia_client import WikipediaClient

# To:
from src.wikipedia_client_alternative import WikipediaClient
```

### Verification

After applying the fix, you should see successful Wikipedia data retrieval:

```
INFO: Retrieving Wikipedia intro for coach: Steffen Baumgart
INFO: Retrieved intro text (XXX chars)
```

Instead of the error message.

### Best Practices for Wikipedia API Usage

1. **Always set User-Agent**: Include application name and contact information
2. **Respect rate limits**: Wikipedia allows reasonable request rates for bots
3. **Cache responses**: Avoid repeated requests for the same data within short timeframes
4. **Handle errors gracefully**: Wikipedia API may be temporarily unavailable
5. **Follow redirects**: Use `redirects=1` parameter to handle page redirects automatically

### User-Agent Format

Wikipedia recommends this format:

```
ApplicationName/Version (ContactURL; contact@email.com)
```

Examples:
```
BundesligaCoachRAGChatbot/1.0 (https://github.com/username/repo; myemail@example.com)
MyBot/2.3 (https://myproject.org/bot; bot-admin@myproject.org)
ResearchProject/1.0 (University of XYZ; researcher@xyz.edu)
```

### Additional Resources

- [Wikimedia User-Agent Policy](https://meta.wikimedia.org/wiki/User-Agent_policy)
- [Wikipedia API Documentation](https://www.mediawiki.org/wiki/API:Main_page)
- [wikipedia-api Python Package](https://pypi.org/project/Wikipedia-API/)

## Other Common Issues

### Issue: "No clubs retrieved from Wikidata"

**Cause**: Wikidata SPARQL endpoint may be temporarily unavailable or query timeout

**Solutions**:
- Check internet connection
- Verify Wikidata endpoint is accessible: https://query.wikidata.org/
- Review SPARQL query in logs for syntax errors
- Increase timeout in `wikidata_client.py`

### Issue: "Could not identify a city or club in your question"

**Cause**: Entity extraction pattern didn't match the query format

**Solutions**:
- Use one of the example question formats:
  - "Who is coaching [City]?"
  - "What about [City]?"
  - "Who is [City]s manager?"
  - "Who is it for [City]?"
- Check for typos in city names
- Ensure city name is in English

### Issue: "No coach found for club"

**Cause**: Coach information not available in Wikidata or not properly linked

**Solutions**:
- Verify the club has a current coach listed on their Wikidata page
- Check if Wikidata uses property P286 (head coach) for that club
- Some clubs may have recently changed coaches and Wikidata hasn't been updated
- This is a data availability issue, not a code issue

## Logging and Debugging

All operations are logged to both console and daily log files:

**Log File Location**: `logs/bundesliga_rag_YYYYMMDD.log`

**Log Directory**: The `logs/` directory is automatically created on first run if it doesn't exist

**Log Levels**:
- Console: INFO and above
- File: DEBUG and above (includes all API requests and responses)

**Debugging Steps**:
1. Reproduce the error
2. Check the log file for detailed error traces
3. Look for API request URLs and responses in DEBUG logs
4. Verify the exact error message and HTTP status code

**Example Debug Log Entry**:
```
2025-10-29 10:30:45 - WikipediaClient - DEBUG - Wikipedia API request params: {...}
2025-10-29 10:30:45 - WikipediaClient - DEBUG - Wikipedia API request headers: {...}
2025-10-29 10:30:46 - WikipediaClient - DEBUG - Raw Wikipedia response: {...}
```

This allows you to trace exactly what data was sent and received, making it easy to identify where false information might have originated.