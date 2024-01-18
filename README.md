<!-- header -->

<div align='center'>
  <img src='static/img/logos/portfolio-logo-240.png' width='75px' alt='Logo'>
  <h1>Portfolio Website</h1>
  <p>
    <i>My personal website and blog.</i>
  </p>
  <p>
    Django | PostgreSQL | htmx | hyperscript | Bootstrap
  </p>
</div>

<!-- images  -->

<div align='center'>
  <h3>Image Gallery</h3>
  <hr/>
  <div class='images-container'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-projects.png' alt='Projects page' width='400px' height='600px'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-post-images.png' alt='Blog post' width='400px' height='600px'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-blog.png' alt='Blog' width='400px' height='600px'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-post-code.png' alt='Blog post with code examples' width='400px' height='600px'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-post-comment.png' alt='Comment form' width='400px' height='600px'>
    <img src='projects/static/projects/img/screenshots/portfolio-600x900-post-search.png' alt='Search results' width='400px' height='600px'>
  </div>
</div>

<!-- installation -->

<div>
  <h3>Running the application</h3>
  <hr/>
  <p>
    In your project directory:
  </p>
  <h4>1. Clone the repository.</h4>
  <p>
    <code>git clone https://github.com/violet-kester/portfolio-website.git</code>
  </p>
  <h4>2. Activate the virtual environment and install dependencies.</h4>
  <p>
   <code>python3 -m venv venv</code><br />
   <code>source venv/bin/activate</code><br />
   <code>pip install -r requirements.txt</code>
  </p>
  <h4>
    3. Create the database.
  </h4>
  <p>
    <code>createdb vk_portfolio_website</code><br/>
  </p>
  <h4>
    4. Configure environment variables.
  </h4>
  <p>
    Create an <code>.env</code> file and add the following values to it:
  </p>
  <p>
    <code>SECRET_KEY=your-secret-key-here</code><br/>
    <code>DB_NAME=vk_portfolio_website</code><br/>
    <code>DB_USER=your-db-username-here</code><br/>
    <code>DB_PASS=your-db-password-here</code><br/>
    <code>DEBUG=True</code>
  </p>
  <h4>
    3. Start the development server.
  </h4>
  <p>
    <code>python manage.py runserver</code>
  </p>
  <h4>
    4. Open the app in your browser at <a href='http://127.0.0.1:8000/'>http://127.0.0.1:8000/</a>.
  </h4>
</div>