#include <iostream>
#include <string>
#include<cmath>
using namespace std;
class Queen {
public:
    
   
    Queen() {};

    void printBoard(int board[8][8]) {
        for (int i = 0; i < 8; i++) {
            cout  << "_______________________________" << endl;
            for (int j = 0; j < 8; j++) {
                cout << "|";
                if (board[i][j] == 1) {
                    cout << " Q ";
                } else {
                    cout << " . ";
                }
            
            }
            cout << endl;
        }
        cout  << "______________________________" << endl;
    }

    int rowConflict(int board[8][8], int row, int col) {
        int conflicts = 0;
        // تحقق من التعارضات في الصف
        for (int c = 0; c < 8; c++)
            // بحث عن ملكة في نفس الصف بشرط ان لا تكون نفس الملكة   
            if (board[row][c] == 1 && c != col)
                conflicts++;
        return conflicts;
    }

    int diagonalConflict(int board[8][8], int row, int col) {
        // تحقق من التعارضات في القطر
        int conflicts = 0;
        for (int x = 0; x < 8; x++) {
            for (int y = 0; y < 8; y++) {
                // بنتاكد انه الي اخترته توا مش نفس الملكة الي اخترتها في البداية
                if (board[x][y] == 1 && !(x == row && y == col))
                    // نطرح في الصفوف من بعض والاعمدة من بعض
                    if (abs(row - x) == abs(col - y))
                        conflicts++;
            }
        }
        return conflicts;
    }
    int countConflict(int board[8][8]) {
        int conflicts = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (board[i][j] == 1) {
                    // تحقق من التعارضات في الصف والقطر
                    conflicts += rowConflict(board, i, j);
                    conflicts += diagonalConflict(board, i, j);
                }
            }
        }
        return conflicts / 2; // كل تعارض يُحسب مرتين
    }

    void copy_board(int (&board)[8][8], int (&temp)[8][8]) {
        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                temp[r][c] = board[r][c];
            }
        }
    }

    int hillClimbing(int (&board)[8][8],int col){
        
        int min_conflicts=9999;
        int best_row=0;
        for (int i=0;i<8;i++){
            int temp_board[8][8];
            // نسخ اللوحة الحالية الى لوحة مؤقتة
            copy_board(board,temp_board);
        //    ازالة الملكة من العمود الحالي
            for (int r=0;r<8;r++){
                temp_board[r][col]=0;
            }
            // وضع الملكة في الصف i من العمود الحالي
            temp_board[i][col]=1;
            
            int conflicts=countConflict(temp_board);
            if(conflicts<min_conflicts){
                min_conflicts=conflicts;
                best_row=i;
            }  
            
             
        }    
        // تحديت موقع الملكة في العمود الحالي الى افضل صف
        for (int r=0;r<8;r++){
            board[r][col]=0;
        }
        board[best_row][col]=1;
        return countConflict(board);
    }

    int simulatedAnnealing(int (&board)[8][8],int iterations){
        double temperature=100;
        double annealing_rate=0.95;
        int temp_board[8][8];
        for(int itr=0;itr<iterations;itr++){
            cout << "iterations: " << itr <<endl;
            cout << "temperature: " << temperature << endl;
            double current_conflict=countConflict(board);
            cout << "conflict: " << current_conflict << endl;
            printBoard(board);
            copy_board(board,temp_board);
            // اختيار موقع عشوائي لوضع الملكة
            int rand_row=rand()%8;
            int rand_col=rand()%8;
            for(int i=0;i<8;i++){
                // نخلي العمود الي اخترته بطريقة عشوائية كله صفار
                temp_board[i][rand_col]=0;  
            }
            // نحط الملكة في الصف العشوائي بعد ماخليت العمود كله قيمته اصفار
            temp_board[rand_row][rand_col]=1;
            double new_conflict=countConflict(temp_board);
            if(new_conflict<current_conflict){
                copy_board(temp_board,board);
            }
            else{
                // احتمالية القبول
                double p = exp(-(fabs(current_conflict-new_conflict)/temperature));
                double r=(double) rand()/RAND_MAX;
                if(p>r){
                    // قبول الحالة الجديدة بحيث ننسخ اللوحة المؤقتة الى اللوحة الرئيسية
                    copy_board(temp_board,board);
                }
            }
            temperature*=annealing_rate;
            if(current_conflict==0){
                cout << "Solved\n";
                break;
            }
        }
        return countConflict(board);
    }

};

int main(){
     int board[8][8]={
        {0,1,1,0,0,0,0,0},
        {0,0,0,0,0,0,0,0},
        {0,0,0,0,0,1,0,0},
        {0,0,0,0,0,0,0,1},
        {1,0,0,0,0,0,0,0},
        {0,0,0,1,0,0,0,0},
        {0,0,0,0,0,0,1,0},
        {0,0,0,0,1,0,0,0}
    }; 
    Queen q;
    int choice;
    cout << "choose algorithm:\n1-hill climbing\n2-simulated annealing\n";
    cin >> choice;
    if(choice==1){
        cout << "start state " << endl;
        q.printBoard(board);
        cout << "count of conflicts: " << q.countConflict(board) << endl;
        for(int c=0;c<8;c++){
            cout <<"=============================================\n";
            cout << "current colum: " << c << endl;
            cout << "count of conflic after edit = "<< q.hillClimbing(board,c) << endl;
            if (q.countConflict(board)==0){
                cout << "Solved\n";
                break;
            }
            q.printBoard(board);
            cout <<"=============================================\n";
        }
    }    
    else if(choice==2){
        cout << "start state " << endl;
        q.simulatedAnnealing(board,100);
    }
    cout << "final state: " << endl;
    q.printBoard(board);    
    return 0;
}