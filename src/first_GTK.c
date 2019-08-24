#include <stdbool.h>
#include <string.h>
#include <gtk/gtk.h>

GdkPixbuf *icon_loader(const gchar *filename) {
  GdkPixbuf *pixbuf;
  GError *error = NULL;
  pixbuf = gdk_pixbuf_new_from_file(filename, &error);
   
  if (!pixbuf) {
    fprintf(stderr, "%s\n", error->message);
    g_error_free(error);
  }

  return pixbuf;
}

void set_window_icon(GtkWidget *window) {
  GdkPixbuf *icon;

  icon = icon_loader("planner.png");  
  gtk_window_set_icon(GTK_WINDOW(window), icon);
  g_object_unref(icon); 
}

GtkWidget *create_window() {
  //init GTK object pointer
  GtkWidget *window;

  //init window
  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title(GTK_WINDOW(window), "Routine Calendar");
  gtk_window_set_default_size(GTK_WINDOW(window), 1366, 768);
  gtk_container_set_border_width(GTK_CONTAINER(window), 15);
  gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);

  g_signal_connect(
    window, 
    "destroy",
    G_CALLBACK(gtk_main_quit), 
    NULL
  );

  return window;
}

void print_msg(GtkWidget *widget, gpointer window) {
  g_print("Button clicked\n");
}

GtkWidget *create_button(char label[], bool is_mnemonic) {
  GtkWidget *button;

  if (is_mnemonic) {
    char _label[strlen(label)+1];
    char underscore[1];
    underscore[0] = '_';
    strcpy(_label, underscore);
    strcat(_label, label);
    button = gtk_button_new_with_mnemonic(_label);
  } else
    button = gtk_button_new_with_label(label);
  gtk_widget_set_tooltip_text(button, "Button widget");

  g_signal_connect(
    button, 
    "clicked", 
    G_CALLBACK(print_msg), 
    NULL
  );
  
  return button;
}

GtkWidget *create_container() {
  GtkWidget *container;

  container = gtk_alignment_new(0, 0, 0, 0);
  
  return container;
}

void add_to_container(GtkWidget *container, GtkWidget *window, GtkWidget *field) {
  gtk_container_add(GTK_CONTAINER(container), field);
  gtk_container_add(GTK_CONTAINER(window), container);
}

void add_button(GtkWidget *window, char label[], bool is_mnemonic) {
  GtkWidget *button;
  GtkWidget *container;

  button = create_button(label, is_mnemonic);
  container = create_container();
  add_to_container(container, window, button);
}

void init_main_window() {
  GtkWidget *window;

  window = create_window();
  set_window_icon(window);
  add_button(window, "Button", true);

  gtk_widget_show_all(window);
}

int main(int argc, char *argv[]) {
  //init GTK process
  gtk_init(&argc, &argv);
  init_main_window();  
  gtk_main();

  return 0;
}
