import pygame

class ScoreMaster:
    GRADES = [
            {
            'grade' : 'PERFECT',
            'hit_window': 40.0,
            'score': 50,
            },
            {
            'grade' : 'GREAT',
            'hit_window': 60.0,
            'score': 25, 
            },
            {
            'grade' : 'NORMAL', 
            'hit_window': 120.0,
            'score': 10, 
            },
            { 
            'grade' : 'miss',
            'hit_window': float('inf'),
            'score': 0, 
            },
            {
            'grade' : 'hold',
            'hit_window': float('inf'),
            'score': 5, 
            },        
            ]
    
    COMBOS = {
        0: 1,
        10: 1.5,
        30: 2,
        50: 3,
    }

    def __init__(self):
        self.score = 0
        self.combo_counter = 0
        self.combo_modifier = 1
        self.last_grade = ''

    def judge(self, note_state):
            match note_state:
                case float():
                    G = sorted(self.GRADES, key = lambda x: x['hit_window'])
                    #print(G)

                    for grade in G:
                        target_distance, score = grade['hit_window'], grade['score']
                        if target_distance and note_state <= target_distance:
                            self.score += score * self.combo_modifier
                            self.combo_counter += 1
                            self.last_grade = grade['grade']
                            break
                            #print(distance, float(target_distance)) 
                    #print(self.score, self.combo_modifier, distance)
                    
                case str():
                    for grade in self.GRADES:
                        if grade['grade'] == note_state:
                            score = grade['score']            
                    self.score += score * self.combo_modifier
                    if note_state == 'miss': self.combo_counter = 0

            self._update_combo_modifier()

    def _update_combo_modifier(self):
        for threshold, multiplier in self.COMBOS.items():
            if self.combo_counter >= threshold:
                self.combo_modifier = multiplier
    
    def draw_score(self, screen):
        #ВРЕМЕННО
        font = pygame.font.Font(None, 36)
        score = font.render(str(self.score), True, (0, 0, 0))
        screen.blit(score, (50, 50))
        modifier = font.render('x'+str(self.combo_modifier), True, (0, 0, 0))
        screen.blit(modifier, (50, 100))
        modifier = font.render(str(self.last_grade), True, (0, 0, 0))
        screen.blit(modifier, (50, 150))