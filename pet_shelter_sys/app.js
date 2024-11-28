var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var adoptGridRouter = require('./routes/adoptGrid');
var petDescRouter = require('./routes/petDesc');
var contactUsRouter = require('./routes/contactUs');
var aboutUsRouter = require('./routes/aboutUs');
// Admin Interface
var adminLandingRouter = require('./routes/admin/adminLanding');
var adminLoginRouter = require('./routes/admin/adminLogin');
var adminEncodeRouter = require('./routes/admin/adminEncode');
var adminTableRouter = require('./routes/admin/adminTable');
var adminViewRouter = require('./routes/admin/adminView');
var adminEditRouter = require('./routes/admin/adminEdit');
var adminDeleteRouter = require('./routes/admin/adminDelete');


var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/adoptGrid', adoptGridRouter);
app.use('/petDesc', petDescRouter);
app.use('/contactUs', contactUsRouter);
app.use('/aboutUs', aboutUsRouter);
//Admin Interface
app.use('/admin', adminLandingRouter);
app.use('/admin/login', adminLoginRouter);
app.use('/admin/adminEncode', adminEncodeRouter);
app.use('/admin/adminTable', adminTableRouter);
app.use('/admin/adminView', adminViewRouter);
app.use('/admin/adminEdit', adminEditRouter);
app.use('/admin/adminDelete', adminDeleteRouter);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
