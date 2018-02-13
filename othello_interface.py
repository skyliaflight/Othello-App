import tkinter
import game_classes
import math
import cartesian
        
    

class OptionsWindow:
    def __init__(self) -> None:
        '''
        Sets up the window with its components and the variables
        which hold the results of the input.
        '''
        # Variables to be based on input at interface
        self._no_of_rows = 0
        self._no_of_col = 0
        self._first_player = game_classes.EMPTY
        self._initial_topleft_disc = game_classes.EMPTY
        self._winner_option = ""

        # Window and input components
        self._dialog_window = tkinter.Toplevel()
        #label = tkinter.Label(master = self._dialog_window,
        #                      font = ('Times', '21'), text = "Choose even\nnumbers of rows\nand columns...",
        #                      padx = 10, pady = 15)
        #label.grid(row = 0, column = 0, sticky = tkinter.W)
        self._row_entry = self._entry_field('Rows (Even Number in 4-16)', 1, 0)      
        self._col_entry = self._entry_field('Columns (Even Number in 4-16)', 2, 0)       
        self._first_player_options = self._two_checkbox_options("First Player",
                                                                "Black", "White",
                                                                3, 0)
        self._initial_topleft_disc_options = self._two_checkbox_options("Initial Top-left Disc",
                                                                        "Black", "White", 5, 0)
        self._winner_options = self._two_checkbox_options("Winner Options",
                                                          "Higher Score",
                                                          "Lower Score", 7, 0)
        self.ok_button = tkinter.Button(master = self._dialog_window, text = "Ok",
                                        font = ('Times', '15'),
                                        command = self._ok_button_pressed)
        self.ok_button.grid(row = 9, column = 1, sticky = tkinter.W + tkinter.E, pady = 30, padx = 15)
        self.msg_text = tkinter.StringVar()
        self.msg_text.set("")
        self.msg_label = tkinter.Label(master = self._dialog_window,
                                       textvariable = self.msg_text,
                                       font = ('Times', '15'))
        self.msg_label.grid(row = 9, column = 0, sticky = tkinter.W + tkinter.E)

    def get_no_of_rows(self) -> int:
        return self._no_of_rows

    def get_no_of_col(self) -> int:
        return self._no_of_col

    def get_first_player(self) -> int:
        return self._first_player

    def get_initial_topleft_disc(self) -> int:
        return self._initial_topleft_disc

    def get_winner_mode(self) -> int:
        return self._winner_option

    def show(self) -> None:
        '''
        Makes the window active.
        '''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def _entry_field(self, label_text: str, row_index: int, col_index: int) -> tkinter.Entry:
        '''
        Gives the window an entry field with a label next to it.
        Returns the entry field.
        '''
        label = tkinter.Label(master = self._dialog_window,
                              font = ('Times', '15'), text = label_text,
                              padx = 10, pady = 15)
        label.grid(row = row_index, column = col_index, sticky = tkinter.W)
        entry_field = tkinter.Entry(master = self._dialog_window,
                                    font = ('Times', 15))
        entry_field.grid(row = row_index, column = col_index+1, sticky = tkinter.W, padx = 15)
        return entry_field

    def _two_checkbox_options(self, main_label: str, sublabel_1: str, sublabel_2: str,
                              row_index: int, col_index: int) -> ("tkinter.Checkbutton.variable"):
        '''
        This gives the window two labled checkboxes under a single main label.
        The variables holding the checkbox inputs are returned as a tuple.
        The given indexes should be the top left corner of an available
        Grid space of 2 units high and 4 units wide.
        '''
        label = tkinter.Label(master = self._dialog_window, font = ('Times', '15'),
                              text = main_label, padx = 10, pady = 15)        
        label.grid(row = row_index, column = col_index, sticky = tkinter.W, columnspan = 4)

        checkbox_values = (tkinter.IntVar(), tkinter.IntVar())
        checkbox_1 = tkinter.Checkbutton(master = self._dialog_window, text = sublabel_1, variable = checkbox_values[0])
        checkbox_1.grid(row = row_index+1, column = col_index+0, sticky = tkinter.W + tkinter.E)
        checkbox_2 = tkinter.Checkbutton(master = self._dialog_window, text = sublabel_2, variable = checkbox_values[1])
        checkbox_2.grid(row = row_index+1, column = col_index+1, sticky = tkinter.W + tkinter.E)
        return checkbox_values

    def _ok_button_pressed(self) -> None:
        '''
        Stores the user's input when the ok button is pressed.
        '''
        try:
            self._no_of_rows = OptionsWindow._read_rows_or_col(self._row_entry)
            self._no_of_col = OptionsWindow._read_rows_or_col(self._col_entry)                   
            self._first_player = OptionsWindow._read_player_color(self._first_player_options)
            self._initial_topleft_disc = OptionsWindow._read_player_color(self._initial_topleft_disc_options)
            self._winner_option = OptionsWindow._read_winner_settings(self._winner_options)
            
        except game_classes.InvalidSetting:
            self.msg_text.set("INVALID")
            
        except ValueError:
            self.msg_text.set("INVALID")
            
        else:
            self._dialog_window.destroy()

    def _read_player_color(player_checkbox_options: ("tkinter.Checkbutton.variable")) -> int:
        '''
        This takes a tuple of two Checkbutton.variables, assuming the first represents
        BLACK and the second represents WHITE. Returns the appropriate player color.
        Raises error if neither or both boxes were checked.
        '''
        if player_checkbox_options[0].get() == 1 and player_checkbox_options[1].get() == 0:
            return game_classes.BLACK
        elif player_checkbox_options[0].get() == 0 and player_checkbox_options[1].get() == 1:
            return game_classes.WHITE
        else:
            raise game_classes.InvalidSetting        

    def _read_rows_or_col(rows_or_col_entry: tkinter.Entry) -> int:
        '''
        Reads and validates the entered number of rows and columns.
        '''
        if int(rows_or_col_entry.get())%2 == 0 and int(rows_or_col_entry.get()) >= 4 and int(rows_or_col_entry.get()) <= 16:
            return int(rows_or_col_entry.get())
        else:
            raise game_classes.InvalidSetting        

    def _read_winner_settings(winner_options: ("tkinter.Checkbutton.variable")) -> str:
        '''
        Reads the winner settings and raises an error if necessary.
        '''
        if winner_options[0].get() == 1 and winner_options[1].get() == 0:
            return '>'
        elif winner_options[0].get() == 0 and winner_options[1].get() == 1:
            return '<'
        else:
            raise game_classes.InvalidSetting
        

class OthelloApplication:
    def __init__(self) -> None:
        '''
        Sets up the gameboard window and its components which
        will display the state of the game.
        '''
        self._root_window = tkinter.Tk()
        self._root_window.configure(background = '#B8E5F5')
        self.msg_text = tkinter.StringVar()
        self.msg_text.set("Waiting for user-entered settings...     ")
        self.msg_label = self._heading_label(self.msg_text, 2, 0, 2)   # Create the message label early.     
        
        options_window = OptionsWindow()
        options_window.show()
        self._game = game_classes.GameState(options_window.get_first_player(),
                                            options_window.get_winner_mode(),
                                            options_window.get_no_of_rows(),
                                            options_window.get_no_of_col(),
                                            options_window.get_initial_topleft_disc())        

        # Text variables for the labels
        self.black_score = tkinter.StringVar()
        self.white_score = tkinter.StringVar()
        self.game_version = tkinter.StringVar()
        self.error_msg = tkinter.StringVar()
        self.game_version.set("OTHELLO")

        # Heading labels
        self._black_score_label = self._heading_label(self.black_score, \
                                                      1, 0, 1)
        self._white_score_label = self._heading_label(self.white_score, \
                                                      1, 1, 1)
        self._game_mode_label = self._heading_label(self.game_version, 0, 0, 2)

        # Error label
        self.error_label = tkinter.Label(master = self._root_window,
                              font = ('Times', '12'), textvariable = self.error_msg,
                              padx = 4, pady = 4, justify = tkinter.CENTER,
                              anchor = tkinter.CENTER)
        self.error_label.configure(background = '#B8E5F5')
        self.error_label.grid(row = 3, column = 0, columnspan = 2, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        # Gameboard display
        self._gameboard_display = tkinter.Canvas(master = self._root_window,
                                                 width = 50*self._game.no_of_col(),
                                                 height = 50*self._game.no_of_rows(),
                                                 background = 'white')
        self._gameboard_display.grid(row = 4, column = 0, columnspan = 2,
                                     sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._gameboard_display.bind('<Configure>', self._refresh_game_window)
        self._gameboard_display.bind('<Button-1>', self._on_mouse_click)
        self._gameboard_rectangles = self._cell_display()
        self._gameboard_discs = self._disc_display()

        # Column and row responses to reconfiguring the window
        self._root_window.rowconfigure(4, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

    def run(self) -> None:
        '''
        Makes the window active.
        '''
        self._root_window.mainloop()        

    def _heading_label(self, label_text: str, row_index: int, col_index: int, col_span: int) -> tkinter.Label:
        '''
        Creates a centered label in a heading format and puts it straight into the grid.
        '''
        label = tkinter.Label(master = self._root_window,
                              font = ('Times', '21'), textvariable = label_text,
                              padx = 10, pady = 7, justify = tkinter.CENTER,
                              anchor = tkinter.CENTER)
        label.configure(background = '#B8E5F5')
        label.grid(row = row_index, column = col_index, columnspan = col_span,
                   sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        return label

    def _on_mouse_click(self, event: tkinter.Event):
        '''
        The response when the user clicks on the gameboard display.
        '''
        click_point = cartesian.Point(event.x, event.y, self._gameboard_display.winfo_width(),
                                      self._gameboard_display.winfo_height())
        
        for rect in self._gameboard_rectangles.all_rects():
            if rect.contains(click_point):
                grid_coord = cartesian.index_to_grid_coord(self._gameboard_rectangles.all_rects().index(rect), \
                                                           self._game.no_of_rows(), self._game.no_of_col())               

                try:
                    self._game.player_take_turn(grid_coord[1], grid_coord[0])
                except game_classes.InvalidMoveError:
                    # If the move fails, do not change the
                    # state of the rectangles and circles.
                    self.error_msg.set("Invalid Move")
                else:
                    self._gameboard_discs = self._disc_display()    # Update the displayed discs.
                    self.error_msg.set("")
                    self._game.next_player_turn()
                    self._refresh_game_window(event)

    def _refresh_game_window(self, event: tkinter.Event):
        '''
        Redraws the game to bring the display up to date.
        This is where you will draw the rectangles and circles
        from your RectangleState and CircleState.
        '''
        self.black_score.set("Black's Score: " + \
                             str(self._game.black_score()))
        self.white_score.set("White's Score: " + \
                             str(self._game.white_score()))

        if self._game.get_winner() != None:
            self.msg_text.set("Winner: " + \
                              game_classes.GameState.player_to_string(
                              self._game.get_winner()))
        else:
            self.msg_text.set("Player's Turn: " + \
                              game_classes.GameState.player_to_string(
                              self._game.player_making_move()))
        
        self._gameboard_display.delete(tkinter.ALL)
        
        for rectangle in self._gameboard_rectangles.all_rects():
            self._draw_rect(rectangle)

        for oval in self._gameboard_discs.all_circles():
            # Some places in the Circle-
            # State are expected to contain None.
            if oval != None:
                self._draw_oval(oval)

    def _draw_oval(self, oval: "Circle") -> None:
        '''
        Draws an oval on the canvas.
        '''
        p1, p2 = oval.get_points()
        p1 = p1.px_coord(self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())
        p2 = p2.px_coord(self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())        
        self._gameboard_display.create_oval(p1[0], p1[1], p2[0], p2[1], fill = oval.get_color())        
        
    def _draw_rect(self, rect: "Rectangle") -> None:
        '''
        Draws the rectangle on the gameboard canvas.
        '''
        p1, p2 = rect.get_points()
        p1 = p1.px_coord(self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())
        p2 = p2.px_coord(self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())        
        self._gameboard_display.create_rectangle(p1[0], p1[1], p2[0], p2[1], \
                                            fill = rect.get_color(), \
                                            outline = rect.get_border_color())

    def _disc_display(self) -> cartesian.CircleState:
        '''
        This should create the state of the existing circles,
        which resemble the discs, based on the GameState.
        '''
        gameboard_circles = cartesian.CircleState()

        for row in self._game.get_rows_of_cells():
            for cell in row:
                if cell.cell_content() == game_classes.BLACK:
                    # Use the points of the corresponding rectangle
                    # to determine the points of the new circle.
                    rect_index = cartesian.grid_coord_to_index(self._game.get_rows_of_cells().index(row), \
                                                                row.index(cell), self._game.no_of_col())
                    rect = self._gameboard_rectangles.all_rects()[rect_index]
                    rect_points = rect.get_points()
                    cir = cartesian.Circle(rect_points[0], rect_points[1], 'black')
                    gameboard_circles.append_circle(cir)
                if cell.cell_content() == game_classes.WHITE:
                    # Use the points of the corresponding rectangle
                    # to determine the points of the new circle.
                    rect_index = cartesian.grid_coord_to_index(self._game.get_rows_of_cells().index(row), \
                                                                row.index(cell), self._game.no_of_col())
                    rect = self._gameboard_rectangles.all_rects()[rect_index]
                    rect_points = rect.get_points()
                    cir = cartesian.Circle(rect_points[0], rect_points[1], 'white')
                    gameboard_circles.append_circle(cir)

        return gameboard_circles

    def _cell_display(self) -> cartesian.RectangleState:
        '''
        Creates a bunch of rectangles to be displayed as game
        cells on the canvas.
        '''
        gameboard_rectangles = cartesian.RectangleState()

        for row_index in range(self._game.no_of_rows()):
            for col_index in range(self._game.no_of_col()):
                # Two opposite corner points of the rectangle we are about
                # to create.
                p1 = cartesian.Point((1/self._game.no_of_col())*col_index*self._gameboard_display.winfo_width(),
                                     (1/self._game.no_of_rows())*row_index*self._gameboard_display.winfo_height(),
                                      self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())
                p2 = cartesian.Point((1/self._game.no_of_col())*(col_index+1)*self._gameboard_display.winfo_width(),
                                     (1/self._game.no_of_rows())*(row_index+1)*self._gameboard_display.winfo_height(),
                                      self._gameboard_display.winfo_width(), self._gameboard_display.winfo_height())
                
                gameboard_rectangles.append_rect(cartesian.Rectangle(p1, p2))

        return gameboard_rectangles
    


def run_program():
    '''
    Runs the Othello game program.
    '''
    othello_app = OthelloApplication()
    othello_app.run()


if __name__ == "__main__":
    run_program()
    
 
