navbar = """
  <nav class="navbar">
    <div class="nav-left">
      <div class="logo">LOGO</div>
      <ul class="nav-links">
        <li><a href="/" class="active">Home</a></li>
        <li><a href="/about">About</a></li>
        <li class="dropdown">
          <a href="#">Data Explorer ▾</a>
          <ul class="dropdown-menu">
            <li><a href="#facts">Vaccination</a></li>
            <li><a href="/Infection">Infection</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Insights ▾</a>
          <ul class="dropdown-menu">
            <li><a href="#insights">Vaccination</a></li>
            <li><a href="#insights">Infection</a></li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="nav-right">
      <input type="text" class="search" placeholder="Search">
    </div>
  </nav>
"""