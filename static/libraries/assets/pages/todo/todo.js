  'use strict';
  $(document).ready(function() {

      //  main button click function
      $('button#create-task').on('click', function() {

          $(".md-form-control").removeClass("md-valid");

          // remove nothing message
          if ('.nothing-message') {
              $('.nothing-message').hide('slide', { direction: 'left' }, 300)
          };

          // create the new li from the form input
          var task = $('input[name=task-insert]').val();
          // Alert if the form in submitted empty
          if (task.length == 0) {
              alert('please enter a task');
          } else {
              var newTask = '<li>' + '<p>' + task + '</p>' + '</li>'
              $('#task-list').append(newTask);

              // clear form when button is pressed
              $('input').val('');

              // makes other controls fade in when first task is created
              $('#controls').fadeIn();
              $('.task-headline').fadeIn();
          }

      });

      // mark as complete
      $(document).on('click', 'li', function() {
          $(this).toggleClass('complete');
      });

      // double click to remove
      $(document).on('dblclick', '#task-list li', function() {
          $(this).remove();
      });

      // Clear all tasks button
      $('button#clear-all-tasks').on('click', function() {
          $('#task-list li').remove();
          $('.task-headline').fadeOut();
          $('#controls').fadeOut();
          $('.nothing-message').show('fast');
      });

      /*2nd todo*/
      $(".icofont icofont-ui-delete").on("click", function() {

          $(this).parent().parent().parent().fadeOut();
      });
      var i = 2;
      $("#add-btn").on("click", function() {
          $(".md-form-control").removeClass("md-valid");
          var task = $('.add_task_todo').val();
          if (task == "") {
              alert("please enter task");
          } else {
              var add_todo = $('<div class="to-do-list" id="' + i + '"><div class="checkbox-fade fade-in-primary"><label class="check-task"><input type="checkbox" onclick="check_task(' + i + ')" id="checkbox' + i + '"><span class="cr"><i class="cr-icon icofont icofont-ui-check txt-primary"></i></span><span>' + task + '</span></label></div><div class="f-right"><a onclick="delete_todo(' + i + ');" href="#!" class="delete_todolist"><i class="icofont icofont-ui-delete" ></i></a></div></div>');
              i++;
              $(add_todo).appendTo(".new-task").hide().fadeIn(300);
              $('.add_task_todo').val('');
          }
      });

      $(".delete_todolist").on("click", function() {


          $(this).parent().parent().fadeOut();
      });


      /*3rd todo list code*/
      $("#add_t").on("click", function() {
          //var add_todo = $('<div class="to-do-label" id="' + i + '"><div class="checkbox-fade fade-in-primary"><label class="check-task"><input type="checkbox" onclick="check_label(' + i + ')" id="checkbox' + i + '"><span class="cr"><i class="cr-icon icofont icofont-ui-check txt-primary"></i></span><span class="task-title-sp">' + saveTask + '</span><div class="f-right hidden-phone"><i class="icofont icofont-ui-delete delete_todo" onclick="delete_todo(' + i + ');"></i></div></label></div></div>');
          var add_todo = $('<form method="post"><input type="hidden" name="count" value="' + i + '"/></form><div class="to-do-label" id="' + i + '"><div class="checkbox-fade fade-in-primary"><div class="row"><div class="col-sm-2 task-title-sp">Schedule Data Range ' + i + '</div><div class="col-sm-1"><input type="time" class="form-control mb-1" placeholder="" value="" name="timestart' + i + '"></div><div class="col-sm-1"><input type="time" class="form-control mb-1" placeholder="" value="" name="timeend' + i + '"></div><div class="col-sm-1"></div><div class="col-sm-1"><input type="number" min="0" max="30" class="form-control mb-1" placeholder="" value="" name="set_point' + i + '"></div><div class="col-sm-5"></div><div class="col-sm-1"><div class="f-right hidden-phone"><i class="icofont icofont-ui-delete delete_todo" onclick="delete_todo(' + i + ');"></i></div></div></div></div>');
          i++;
          $(add_todo).appendTo(".task-content").hide().fadeIn(300);
          }

      );

      $(".close_btn").on("click", function() {
          $('.save_task_todo').val('');
      });

      $(".delete_todo").on("click", function() {
          $(this).parent().parent().parent().parent().parent().remove();
      });
  });

  function delete_todo(e) {

      $('#' + e).remove();
  }
  $('.to-do-list input[type=checkbox]').on("click", function() {
      if ($(this).prop('checked'))
          $(this).parent().addClass('done-task');
      else
          $(this).parent().removeClass('done-task');
  });

  function check_task(elem) {
      if ($('#checkbox' + elem).prop('checked'))
          $('#checkbox' + elem).parent().addClass('done-task');
      else
          $('#checkbox' + elem).parent().removeClass('done-task');
  }

  $('.to-do-label input[type=checkbox]').on('click', function() {
      if ($(this).prop('checked'))
          $(this).parent().addClass('done-task');
      else
          $(this).parent().removeClass('done-task');
  });

  function check_label(elem) {
      if ($('#checkbox' + elem).prop('checked'))
          $('#checkbox' + elem).parent().addClass('done-task');
      else
          $('#checkbox' + elem).parent().removeClass('done-task');
  }
