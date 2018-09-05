#include <iostream>
#include <vector>
#include <string>
#include <random>

using namespace std;

void test(){
	char maze [10][10] = { '0', '0',
					     '0', '0' };
	int nrows = 2, ncols = 2;

	for (int i = 0; i < nrows; ++i){
		for (int j = 0; j < ncols; ++j){
			cout << maze[i][j];
		} cout << endl;
	}

	string maz [2] = { "000000", "000000"};

	for (int i = 0; i < 2; ++i){
		for (int j = 0; j < maz[0].length(); ++j){
			cout << maz[i][j];
		} cout << endl;
	}
}

void clean(vector<char>& movements){
	for( int i = 1 ; i < movements.size() ; i++){
		if( movements[i-1] == 'L' && movements[i] == 'R' || movements[i-1] == 'R' && movements[i] == 'L' ){
			movements[i-1] = movements[i] = ' ';
		}
		if( movements[i-1] == 'D' && movements[i] == 'U' || movements[i-1] == 'U' && movements[i] == 'D' ){
			movements[i-1] = movements[i] = ' ';
		}
	}

	cout << "Cleaned Path\n";
	vector<char> c_movements;
	for( int i = 0 ; i < movements.size() ; i++){
		if (movements[i]!= ' '){
			c_movements.push_back(movements[i]);
		}
		//cout << movements[i];
	} //cout << endl;

	movements = c_movements;
}

int main(int argc, char const *argv[])
{
	/*string maz [10] = {	"1010000110",
					   	"0100100000",
					   	"0100000010",
					   	"1001010100",
					   	"1000001001",
					   	"0011010111",
					   	"1000000000",
					   	"1011100110",
					   	"0000000010",
					   	"0101010101"};
					   	*/
	string maz [10] = {	"* *    ** ",
					   	" *  *     ",
					   	" *      * ",
					   	"*  * * *  ",
					   	"*     *  *",
					   	"  ** * ***",
					   	"*         ",
					   	"* ***  ** ",
					   	"        * ",
					   	" * * * * *"};

    cout << "Initial Status\n";

	for (int i = 0; i < 10; ++i){
		for (int j = 0; j < maz[0].length(); ++j){
			cout << maz[i][j];
		} cout << endl;
	}

	uniform_real_distribution<double> dist( 0, 1 );
	default_random_engine rng( random_device{}() );

	int steps = 10000; int init_x = 9, init_y = 0; int reward = 0;
	maz[init_x][init_y] = 'o';
	int tmp_x, tmp_y;

	cout << "Initial Reward: " << reward << endl;
	vector<char> movements; int tmp_reward;
	//for( int i = 0 ; i < steps; i++){

	int num_iter = 0;

	while( init_x != 0 && init_y != 9 ){
		num_iter++;
		
		double mov = dist(rng);
		//cout << mov << endl;

		tmp_x = init_x;
		tmp_y = init_y;

		cout << "( " << init_x << ", " << init_y << ")" << endl;
		char m;
		if( 0.0 < mov && mov <= 0.25 ){
			init_x -= 1; m = 'U'; cout << m;
		}
		else if( 0.25 < mov && mov <= 0.50 ){
			init_y += 1; m = 'R'; cout << m;
		}
		else if( 0.50 < mov && mov <= 0.75 ){
			init_x += 1; m = 'D'; cout << m;
		}
		else if( 0.75 < mov && mov <= 1.00 ){
			init_y -= 1; m = 'L'; cout << m;
		} cout << endl;
		movements.push_back(m);
		cout << "( " << init_x << ", " << init_y << ") == > ";

		tmp_reward = reward;

		if( 0 > init_x || init_x > 9 ){ reward -= 15; init_x = tmp_x; }
		else if( 0 > init_y || init_y > 9 ){ reward -= 15; init_y = tmp_y; }
		else if( maz[init_x][init_y] == '*'){ init_x = tmp_x; init_y = tmp_y; }
		else{
			if( maz[init_x][init_y] == ' ' ){ reward += 10; maz[init_x][init_y] = 'o'; maz[tmp_x][tmp_y] = ' '; }
			else if( maz[init_x][init_y] == '*' ){ reward -= 10; }
		}
		if(reward <= tmp_reward){
			movements.pop_back();
		}
		cout << "( " << init_x << ", " << init_y << ")" << endl;

		for (int i = 0; i < 10; ++i){
			for (int j = 0; j < maz[0].length(); ++j){
				cout << maz[i][j];
			} cout << endl;
		} 
		cout << "Reward: " << reward << endl;
		cout << endl;
	}

	cout << "Final Path\n";
	for( int i = 0 ; i < movements.size() ; i++){
		cout << movements[i];
	} cout << endl;

	clean(movements);
	
	for( int i = 0 ; i < movements.size() ; i++){
		cout << movements[i];
	} cout << endl;

	int tmp_size = 1, size_m = 1;

	while( true ){
		tmp_size = movements.size();
		clean(movements);
		
		for( int i = 0 ; i < movements.size() ; i++){
			cout << movements[i];
		} cout << endl;
		size_m = movements.size();

		if( size_m == tmp_size ){ break; }
	}

	cout << "# iter: " << num_iter << endl;

	return 0;
}