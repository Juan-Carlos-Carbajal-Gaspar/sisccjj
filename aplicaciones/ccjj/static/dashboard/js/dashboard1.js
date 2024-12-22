$(function () {

    /* initialize the calendar
    -----------------------------------------------------------------*/
    var Calendar = FullCalendar.Calendar;
    
    var calendarEl = document.getElementById('calendar');

    // initialize the external events
    // -----------------------------------------------------------------
    var calendar = new Calendar(calendarEl, {
      headerToolbar: {
        left  : 'prev,next today',
        center: 'title',
        right : 'dayGridMonth,listMonth,timeGridDay'
      },
      locale: 'es',
      themeSystem: 'bootstrap',
      //Random default events
      events: {
        url: window.location.pathname,
        method: 'POST',
        extraParams: {
            'action': 'searcheventos'
        },
        
      },
      
      editable  : false,
      droppable : false, // this allows things to be dropped onto the calendar !!!
    });

    calendar.render();
    // $('#calendar').fullCalendar()

})