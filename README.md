<ol>
    <h1>An AI Agent reading a local database with a voice interface
    based on twillio </h1>
Setup is based on:
https://www.twilio.com/en-us/blog/voice-ai-assistant-openai-realtime-api

  <h2><li>Create .env file</li></h2>
  First create a .env file in the root directory of your project.
  edit it with text editor and add the following line:
    <pre><code>
    OPENAI_API_KEY=your_openai_api_key
    </code></pre>

  <h2><li>You can start the server</li></h2>
  <p>Use command
  <pre><code>uvicorn main:app --host 0.0.0.0 --port 5050</code></pre></p>
  if you want to change the port number you can add the following line to .env file<pre><code>PORT=your_port_number</code></pre>
  <h2><li>Set up a port tunneling service</li></h2>
  In this example we use zrok.
  Download and register to zrok. Afterwards run following commands:
    <pre><code>zrok enable YOUR_TOKEN </code>
<code>zrok share public --headless http://localhost:5050</code></pre>
  <h2><li>Configure twillio</li></h2>
  Set up a twillio account and get a phone number. 
  Configure the webhook to point to your server's URL (from the port tunneling service)
  followed by /incoming-call endpoint.
</ol>
<h2>References</h2>
code based on:
https://www.twilio.com/en-us/blog/voice-ai-assistant-openai-realtime-api-python