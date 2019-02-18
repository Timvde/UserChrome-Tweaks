/*
 * Description: Personnal toolbar in vertical position on the left
 *              side of firefox's window 
 *
 * Screenshot: https://imgur.com/bjyJH9X
 *
 * Contributor(s): erlotinib
 */

:root {
  /* The space between the top of the window and
   * the beginning of the toolbar may change 
   * between OS/density/...
   * This variable may need to be adjusted in 
   * order to have the bar at the right place
   */
  --space-from-top-of-window: 80px;
}

/* ---------------- */
/*
 * Code from Faviconized Bookmarks from Okamoi
 */

#PersonalToolbar .bookmark-item > .toolbarbutton-text  {
  display: none !important;
}

#PersonalToolbar .bookmark-item > .toolbarbutton-icon  {
  margin-inline-end: 0px !important;
}
/* ---------------- */

/* Create space in the window for the toolbar  */
#browser, #browser-bottombox {
  margin-left: 35px!important;
}

#PersonalToolbar, #personal-bookmarks {
  padding: 0!important;
  margin: 0!important;
}

/* Hide the toolbar when in fullscreen mode */
#main-window[inFullscreen="true"] #PersonalToolbar {
  visibility: collapse !important;
}

#main-window[inFullscreen="true"] #browser,
#main-window[inFullscreen="true"] #browser-bottombox {
  margin-right: 0!important;
}

#PersonalToolbar {
  position: fixed!important;
  /*
   * We place the toolbar below the url-bar and menu bar
   * 0 is the top of firefox's interface 
   */
  top: var(--space-from-top-of-window)!important;
  left:35px;
  height: 35px!important;
  width: 100%!important;
  /* turns the personnalToolbar on its side to a vertical orientation */
  transform-origin: top left!important;
  transform: rotate(90deg)!important;
}

#personal-bookmarks {
  height: 100%!important;
  width: 100%!important;
}

#personal-bookmarks .bookmark-item {
  /*
   * Icons are on their side due to the 90° rotation.
   * Put them back with a rotation, 90° CCW 
   */
  transform: rotate(-90deg)!important;
  /* 
   * Modify width to change space between icon, the value cannot 
   * be greater than the height of #PersonnalToolbar
   */
  width: 35px!important;
  margin-top:0!important;
}
