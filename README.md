# Context Retrieval Script for Germany's 1. Bundesliga Coach RAG-Chatbot

This is a Python application for information retrieval in a RAG (Retrieval-Augmented Generation) chatbot about football club coaches in Germany's 1. Bundesliga. This is a coding challenge developed by PANTOPIX. The coding challenge document "Coding Challenge - KE.pdf" is in the repository folder "coding challenge document" [Coding Challenge - KE.pdf](Coding Challenge - KE.pdf)

## Overview

This system retrieves up-to-date information about Germany's 1. Bundesliga football clubs and their current coaches from Wikipedia and Wikidata. It processes user queries in colloquial format and builds complete prompts for LLM consumption, including system instructions, retrieved context, and the user's question.

## Requirements

- Python 3.8 or higher
- Internet connection (for Wikidata and Wikipedia API access)
- pip (Python package installer)
- Optional: pipenv for dependency management

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd bundesliga-coach-rag

# Using pipenv (recommended)
pipenv install
pipenv run python main.py

# OR using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Installation

There are two ways to set up the project: using **venv** (standard) or **pipenv** (recommended for dependency management).

### Method 1: Using venv (Standard Python)

#### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd bundesliga-coach-rag
```

#### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Run the Application

```bash
python main.py
```

### Method 2: Using pipenv (Recommended)

Pipenv combines package management and virtual environment into a single tool, providing better dependency resolution and security features.

#### Step 1: Install pipenv (if not already installed)

```bash
pip install pipenv
```

#### Step 2: Clone the Repository

```bash
git clone <repository-url>
cd bundesliga-coach-rag
```

#### Step 3: Install Dependencies

```bash
# Install all dependencies from Pipefile.lock and create virtual environment automatically
pipenv install

# Or install from requirements.txt if Pipfile doesn't exist
pipenv install -r requirements.txt
```

#### Step 4: Run the Application

```bash
# Run directly with pipenv
pipenv run python main.py

# Or activate the shell first
pipenv shell
python main.py
```

### Optional: Wikipedia-API Library

If you experience issues with the Wikipedia API (403 Forbidden errors), you can optionally install the `wikipedia-api` library:

**Using venv:**
```bash
pip install wikipedia-api
```

**Using pipenv:**
```bash
pipenv install wikipedia-api
```

Then use the alternative implementation by modifying `main.py`:
```python
# Change this line:
from src.wikipedia_client import WikipediaClient
# To this:
from src.wikipedia_client_alternative import WikipediaClient
```

### Choosing Between venv and pipenv

| Feature | venv | pipenv |
|---------|------|--------|
| **Setup** | Built into Python 3.3+ | Requires separate installation |
| **Dependency Management** | Manual (requirements.txt) | Automatic (Pipfile + Pipfile.lock) |
| **Dependency Resolution** | Basic | Advanced with conflict detection |
| **Security** | Manual checking | Automatic vulnerability scanning |
| **Lock File** | No | Yes (Pipfile.lock) |
| **Best For** | Simple projects, standard workflow | Team projects, production deployments |

**Recommendation**: 
- Use **venv** if you prefer standard Python tools and simple setup
- Use **pipenv** if you want better dependency management and are working in a team environment

## Troubleshooting

### Wikipedia API 403 Forbidden Error

If you encounter a `403 Forbidden` error when accessing Wikipedia:

**Cause**: Wikipedia API requires proper User-Agent headers to identify the client application.

**Solution 1** (Default): The updated `wikipedia_client.py` now includes proper User-Agent headers:
```python
headers = {
    "User-Agent": "BundesligaCoachRAGChatbot/1.0 (https://github.com/user/repo; contact@example.com)"
}
```

**Solution 2**: Use the alternative implementation with `wikipedia-api` library (see Optional Installation above).

**Note**: If deploying this application, replace the contact information in the User-Agent string with your actual project URL and contact email.

## Usage

### Running the Application

```bash
python main.py
```

### Example Interactions

```
Your question: Who is coaching Berlin?

=============================================================
GENERATED LLM PROMPT:
=============================================================
SYSTEM PROMPT:
SYSTEM PROMPT:
You are a helpful assistant an expert in Germany`s 1. Bundesliga football (soccer).
You answer questions about coaches of clubs in Germany's 1. Bundesliga.
You must use only the information provided in the retrieved context below. You must never assume.
Be concise but informative in your responses.
Provide the coach's name and relevant information about them.

RETRIEVED CONTEXT:
City: Berlin
Club: 1. FC Union Berlin
Current Coach: Steffen Baumgart

Coach Information from Wikipedia:
Steffen Baumgart is a Danish professional football manager...

USER QUESTION:
Who is coaching Berlin?

Please answer the user's question using the provided context.
=============================================================
```

The system supports various colloquial question formats:
- "Who is coaching Berlin?"
- "What about munich?"
- "Who is heidenheims manager?"
- "Who is it for Pauli?" (special case for FC St. Pauli)

## System Architecture

### Project Structure

```
bundesliga-coach-rag-chatbot/
├── README.md
├── TROUBLESHOOTING.md
├── requirements.txt           # For pip/venv
├── Pipfile                    # For pipenv
├── .gitignore
├── main.py
├── logs/                      # Auto-created on first run
│   └── bundesliga_rag_YYYYMMDD.log
└── src/
    ├── __init__.py
    ├── logger_config.py
    ├── entity_extractor.py
    ├── wikidata_client.py
    ├── wikipedia_client.py
    ├── wikipedia_client_alternative.py
    └── prompt_builder.py
```

### Components

1. **Entity Extractor** (`src/entity_extractor.py`)
   - Extracts city/club identifiers from user questions
   - Handles case-insensitive input
   - Supports multiple question formats

2. **Wikidata Client** (`src/wikidata_client.py`)
   - Queries Wikidata via SPARQL
   - Retrieves current Bundesliga clubs
   - Retrieves current coach for each club (on every question)

3. **Wikipedia Client** (`src/wikipedia_client.py`)
   - Retrieves coach biographical information
   - Gets introduction paragraph from Wikipedia articles (on every question)

4. **Prompt Builder** (`src/prompt_builder.py`)
   - Constructs final LLM prompt
   - Includes system prompt, retrieved context, and user question

5. **Main Application** (`main.py`)
   - Orchestrates all components
   - Provides console-based interface
   - Handles errors gracefully

### Data Flow

```
User Question (Console Input)
    ↓
Entity Extraction (city/club identification)
    ↓
Club Matching (find Bundesliga club)
    ↓
Wikidata Query (get current coach) ← Retrieved on every question
    ↓
Wikipedia Query (get coach bio) ← Retrieved on every question
    ↓
Prompt Building (system + context + question)
    ↓
Final LLM Prompt (Console Output)
```

## Logging

The system implements comprehensive logging for debugging:

- **Console Output**: INFO level messages for user visibility
- **Log File**: DEBUG level messages in `logs/bundesliga_rag_YYYYMMDD.log`
- **Log Directory**: The `logs/` directory is automatically created on first run if it doesn't exist

Logs capture:
- All Wikidata SPARQL queries and responses
- All Wikipedia API calls and responses
- Entity extraction results
- Data processing steps
- Errors and warnings

This enables tracing the origin of any false answers by examining the log file.

## Error Handling

The system handles the following error scenarios gracefully:

1. **Entity Not Found**: User input doesn't contain recognizable city/club
2. **Club Not Found**: City not associated with Bundesliga club
3. **Coach Data Missing**: No coach information available in Wikidata
4. **Wikipedia Article Missing**: Coach doesn't have Wikipedia article (non-fatal)
5. **Network Errors**: API timeouts or connection failures

All errors return user-friendly messages explaining the issue.

## Special Cases

### Hamburg (Two Clubs)

Hamburg has two Bundesliga clubs:
- **Hamburger SV**: Use "hamburg" or "Hamburg"
- **FC St. Pauli**: Use "pauli" or "Pauli"

### Case Insensitivity

The system handles all case variations:
- "Berlin", "berlin", "BERLIN" all work identically

## Technical Decisions

### Clubs Data Caching

**Decision**: Cache Bundesliga clubs list on startup

**Rationale**: 
- Clubs in a season don't change during a session
- Reduces API load on Wikidata
- Improves response time
- Challenge explicitly allows this choice

### Coach Data Retrieval

**Decision**: Query Wikidata and Wikipedia on every question

**Rationale**:
- Challenge explicitly requires this: "should be retrieved on every question"
- Ensures up-to-date coach information
- Handles recent coaching changes

### Error Handling Philosophy

**Decision**: Graceful degradation with informative messages

**Rationale**:
- Challenge requires handling missing data "in a way that makes sense for the user"
- System continues operation when possible
- Users receive actionable error messages

## Limitations

1. **Language**: Currently uses English Wikipedia; German coaches may have better information in German Wikipedia
2. **Temporal Data**: SPARQL queries for "current" coach may not handle very recent changes (within hours)
3. **Name Matching**: Coach names must match between Wikidata and Wikipedia exactly
4. **Network Dependency**: Requires active internet connection; no offline mode

## Future Improvements

- Support for multiple languages (German Wikipedia)
- Local caching of coach information with TTL
- Fuzzy matching for city/club names
- Historical coach queries
- Support for other German leagues (2. Bundesliga, etc.)

---

## Answers to Additional Questions

### 1. Advantages and Disadvantages of Using Additional Information

**Advantages:**

- **Accuracy**: LLMs have knowledge cutoffs and may have outdated information about current coaches. Real-time retrieval ensures accuracy.
- **Reduces Hallucination**: Providing factual context prevents the LLM from generating plausible but incorrect information.
- **Transparency**: Sources can be traced and verified (from the sources Wikidata and Wikipedia).
- **Domain-Specific Knowledge**: LLMs may not have detailed information about all coaches in the world they are limited to their training dataset; Wikipedia provides comprehensive biographies.
- **Up-to-date Information**: In football coach changes are frequent; therefore real time retrieval captures current data.
- **Confidence**: Users can trust the answers backed by authoritative and verifiable sources.

**Disadvantages:**

- **Latency**: Each query requires multiple API calls (to Wikidata endpoint and Wikipedia API), this can add seconds per request.
- **Complexity**: The system requires more components and a discrete distribution of functions (data retrieval, parsing, error handling).
- **Failure Points**: Because of realtime queries and calls, there could be network issues, API downtime, or missing data these can cause failures.
- **Cost**: commercial API calls consume resources (though Wikidata/Wikipedia are free, commercial alternatives are not free).
- **Maintenance**: Possible changes to Wikidata schema or Wikipedia API will require code updates.
- **Over-reliance on Sources**: Peradventure the data source is incorrect, the answer will be incorrect (garbage in, garbage out).

**Use Case Suitability:**

For this Germany`s 1. Bundesliga football coach Context Retrieval Script for a RAG-Chatbot , the advantages outweigh disadvantages because:
- The need for real time queries because coaching changes are frequent and recent
- The need for accuracy is critical for factual questions
- The two data sources Wikipedia and Wikidata are authoritative and verifiable sources for sports data

### 2. Advantages and Disadvantages of Querying Data on Every Request

**Advantages:**

- **Always Current**: Coaching changes are reflected immediately; no stale data.
- **No Cache Invalidation**: Eliminates complexity of cache management and TTL policies.
- **Simplicity**: No need to implement cache storage, expiration, or update mechanisms.
- **Memory Efficiency**: No in-memory or disk storage required for cached data.
- **Consistency**: All users always see the same, most recent data.
- **No Race Conditions**: Eliminates cache coherency issues in distributed systems.

**Disadvantages:**

- **Performance**: Every request takes seconds for API calls instead of milliseconds for cache hits.
- **API Load**: Constant quering increases load on Wikidata and Wikipedia servers.
- **Rate Limiting Risk**: In most cases frequent queries may trigger rate limits on public APIs.
- **Network Dependency**: Sometimes the system may fail if APIs are temporarily unavailable.
- **Cost**: In commercial settings, pay-per-request APIs may become expensive.
- **User Experience**: Users experience delays for every query, even repeated ones.

**Optimal Strategy:**

A hybrid approach using caching would be ideal:
- **Cache** clubs list (changes seasonally).
- **Cache** coach data with short TTL (e.g., 1 hour) to balance freshness and performance.
- **Cache** Wikipedia intros with longer TTL (24 hours) since coach biographies rarely change.

For this challenge, querying on every request was required for coach data, demonstrating real-time retrieval capability.

### 3. Process Change if Coach Information Only Available via PDF

**Required Changes:**

**1. PDF Acquisition:**
- Implement web scraping or API to download PDF files
- Store PDFs locally or in temporary storage
- Handle PDF versioning and updates

**2. PDF Processing Pipeline:**
- Use libraries like PyPDF2, pdfplumber, or Apache Tika for text extraction
- Implement OCR (Tesseract) for scanned/image-based PDFs
- Handle multi-page documents and complex layouts

**3. Information Extraction:**
- Implement Named Entity Recognition (NER) to extract coach names
- Use pattern matching or NLP to identify relevant sections
- Extract structured data from unstructured text

**4. Data Quality:**
- Implement validation to ensure extracted data is correct
- Handle inconsistent formatting across PDFs
- Deal with incomplete or missing information

**5. Performance:**
- PDF parsing is CPU-intensive; it is important to implement caching
- Consider background processing for large PDFs
- May need to pre-process PDFs rather than real-time extraction

**Code Changes:**

```python
# New component: PDF Processor
class PDFProcessor:
    def extract_coach_info(self, pdf_path):
        # Extract text from PDF
        # Parse and identify coach information
        # Return structured data
        
# Modified workflow:
# 1. Download/locate PDF
# 2. Extract text
# 3. Parse coach information
# 4. Build prompt with extracted data
```

**Challenges:**
- PDFs lack semantic structure (no "coach" tag)
- Formatting varies (tables, lists, paragraphs)
- Scanned PDFs require OCR (error-prone)
- No standard schema for sports data in PDFs
- Real-time processing is slow

**Comparison:**
- Wikipedia API provides structured, clean data instantly
- PDFs require complex parsing with lower accuracy
- This demonstrates why structured knowledge bases (Wikidata) are superior to unstructured documents (PDFs) for RAG systems

### 4. Potential for Agents in This Process

**Yes, agents would add significant value. Here's where and how:**

**4.1 Query Understanding Agent**

**Where:** Entity extraction and query interpretation

**How:** 
- Use an LLM agent to understand ambiguous queries
- Handle complex questions: "Who coaches the team that won the championship last year?"
- Resolve entities through reasoning: "Who's managing the club from the capital?" → Berlin → Union Berlin
- Ask clarification questions when ambiguous

**4.2 Data Retrieval Planning Agent**

**Where:** Determining which data sources to query and in what order

**How:**
- Decide whether Wikidata, Wikipedia, or both are needed
- Determine if additional context is required (club history, league standings)
- Adaptively handle missing data by finding alternative sources
- Optimize retrieval order based on query type

**4.3 Validation Agent**

**Where:** Verifying retrieved data consistency

**How:**
- Cross-reference Wikidata and Wikipedia for inconsistencies
- Flag potentially outdated information
- Verify coaching dates and current status
- Detect contradictions between sources

**4.4 Response Generation Agent**

**Where:** Building tailored responses based on context

**How:**
- Adapt response style to user question (technical vs. casual)
- Include relevant historical context when appropriate
- Suggest follow-up questions
- Explain limitations when data is uncertain

**4.5 Multi-Step Reasoning Agent**

**Where:** Complex queries requiring multiple retrieval steps

**How:**
Example: "Compare the careers of coaches in Hamburg"
1. Identify Hamburg has two clubs
2. Retrieve both coaches
3. Get career data for each
4. Synthesize comparison
5. Generate response

**Implementation Example:**

```python
class CoachQueryAgent:
    def process_query(self, query):
        # Step 1: Understand intent
        intent = self.understand_intent(query)
        
        # Step 2: Plan retrieval strategy
        plan = self.create_retrieval_plan(intent)
        
        # Step 3: Execute plan
        data = self.execute_plan(plan)
        
        # Step 4: Validate data
        validated = self.validate_data(data)
        
        # Step 5: Generate response
        return self.generate_response(validated, query)
```

**Benefits:**
- Handles edge cases and ambiguity
- Provides more intelligent error recovery
- Enables complex, multi-turn conversations
- Adapts to user needs dynamically

**Current System vs. Agentic:**
- Current: Rule-based pipeline (extract → retrieve → build)
- Agentic: Adaptive reasoning with tool use and planning

### 5. How domain data models benefit these processes?

**A domain data model (ontology) provides immense benefits:**
Based on the articles from https://graphwise.ai/fundamentals/what-is-graph-rag/ , 
https://www.elastic.co/search-labs/blog/rag-graph-traversal and https://aerospike.com/blog/introduction-to-graph-rag/

**5.1 Structured Knowledge Representation**

**Benefit:** 
Wikidata's data model defines clear relationships:
- Club → head_coach (P286)
- Club → league (P118)
- Club → location (P159)

This structure enables:
- Direct property queries instead of text parsing
- Relationship traversal (club → coach → nationality → country)
- Inference (if club in Bundesliga, then German league)

**5.2 Semantic Consistency**

**Benefit:**
Standardized entities ensure:
- "FC Bayern München" and "Bayern Munich" map to same entity (Q15789)
- No ambiguity between different clubs named "Union"
- Temporal relationships are explicit (current vs. former coach)

**5.3 Query Efficiency**

**Benefit:**
SPARQL queries leverage the data model:
- Direct property access vs. full-text search
- Graph traversal for complex relationships
- Efficient filtering and aggregation

**Without Data Model (Plain Text):**
```
"The coach of Bayern Munich is Thomas Tuchel"
→ Requires NLP to extract relationships
→ Ambiguous temporal reference (current? as of when?)
→ Name variations cause mismatches
```

**With Data Model (Wikidata):**
```sparql
wd:Q15789 wdt:P286 ?coach  # Direct property access
→ Unambiguous, structured, queryable
→ Temporal qualifiers available
→ Standardized entity identifiers
```

**5.4 Inference and Reasoning**

**Benefit:**
Ontologies enable:
- Transitivity: Club → City → Country → Continent
- Class hierarchies: Coach is-a Person, Club is-a Organization
- Property constraints: head_coach must be a Person

**Example:**
```
Query: "Show all clubs in cities over 1 million population"
→ Requires: Club → City → Population
→ Data model makes this relationship explicit and queryable
```

**5.5 Data Quality and Validation**

**Benefit:**
Schema constraints ensure:
- Coaches must be people (not buildings or concepts)
- Clubs must participate in exactly one league at a time
- Dates are properly formatted and temporal

**5.6 Interoperability**

**Benefit:**
Standardized models enable:
- Integration with other sports databases
- Mapping to Wikipedia, DBpedia, OpenStreetMap
- Consistent data exchange formats

**5.7 Evolution and Maintenance**

**Benefit:**
Structured models support:
- Schema versioning (property changes over time)
- Deprecation of outdated properties
- Community-driven improvements

**Application to This Challenge:**

The Wikidata data model directly enabled:
1. **Entity Resolution**: "Berlin" → 1. FC Union Berlin (Q161697)
2. **Relationship Queries**: Club → current head_coach
3. **Temporal Accuracy**: Current vs. historical coaches
4. **Data Quality**: Validated, community-maintained information

**Comparison with Unstructured Data:**

| Aspect | Structured Model (Wikidata) | Unstructured (Wikipedia Text) |
|--------|---------------------------|----------------------------|
| Query Speed | Milliseconds (SPARQL) | Requires NLP parsing |
| Accuracy | High (validated relationships) | Variable (ambiguous text) |
| Temporal | Explicit qualifiers | Implicit in text |
| Relationships | Direct property access | Must infer from context |
| Maintenance | Community-driven schema | Manual text parsing updates |

**Conclusion:**

Domain data models transform RAG systems from "search and hope" to "query and know." They provide the semantic foundation that makes retrieval accurate, efficient, and reliable. For sports data specifically, ontologies like Wikidata's football domain model are essential for building trustworthy AI systems. 

---

## License

This project as part of a coding challenge developed by Pantopix.

## Documentation

- 📖 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed installation instructions
- 🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## Contact

For questions or issues, please refer to the coding challenge document "Coding Challenge - KE.pdf" in the repository in the folder "coding challenge document".