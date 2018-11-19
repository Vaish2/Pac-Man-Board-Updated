from pacman import pacman

if __name__ == '__main__':
    final_pos_x, final_pos_y, coins_collected = pacman('test.txt')
    print "The final position is (%d, %d).\nThe total no. of coins collected are %d." % (final_pos_x, final_pos_y, coins_collected)
