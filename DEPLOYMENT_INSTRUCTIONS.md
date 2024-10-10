# Deploying to Streamlit Cloud

To deploy this Streamlit app to Streamlit Cloud, follow these steps:

1. Create a GitHub repository and push your project files to it.

2. Go to https://streamlit.io/cloud and sign in with your GitHub account.

3. Click on "New app" and select your GitHub repository.

4. Set the main file path to "main.py".

5. In the "Advanced settings" section, add the following environment variables:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET

   Make sure to use the same values you've been using in your local development environment.

6. Before deploying, make sure to install all required packages by running:
   ```
   pip install -r requirements.txt
   ```

7. Click "Deploy" to start the deployment process.

8. Once deployed, Streamlit Cloud will provide you with a URL for your app.

9. Update your Google Cloud Console project to add the new Streamlit Cloud URL to the list of authorized redirect URIs.

Note: Make sure your GitHub repository is public or that you have linked your GitHub account with Streamlit Cloud for private repositories.

Remember to keep your client ID and client secret secure and never commit them directly to your repository.
