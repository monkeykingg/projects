
import java.sql.*;
import java.util.List;
import java.util.ArrayList;

// If you are looking for Java data structures, these are highly useful.
// Remember that an important part of your mark is for doing as much in SQL (not Java) as you can.
// Solutions that use only or mostly Java will not receive a high mark.
public class Assignment2 extends JDBCSubmission {

    public Assignment2() throws ClassNotFoundException {

        Class.forName("org.postgresql.Driver");
    }

    @Override
    public boolean connectDB(String url, String username, String password) {
        // Implement this method!
        try{
        	connection = DriverManager.getConnection(url, username, password);
        	PreparedStatement ps = connection.prepareStatement("SET search_path TO parlgov;");
        	ps.execute();
        	return true;
        }catch(SQLException SQLE){
        	return false;
        }
    }

    @Override
    public boolean disconnectDB() {
        // Implement this method!
        try{
        	connection.close();
        	return true;
        }catch(SQLException SQLE){
        	return false;
        }
    }

    @Override
    public ElectionCabinetResult electionSequence(String countryName) {
        // Implement this method!

    	// Init parameters for datebase connection and sql excution
    	PreparedStatement ps;
    	ResultSet r;
    	try{

    		// to get election ids and cabinet ids for final list output
    		String getIds = "select temp.election_id, cabinet.id "
                              + "from (select election.id as election_id, e_date "
                                    + "from election, country "
                                    + "where country.name = ? and country.id = election.country_id) temp "
                              + "left join cabinet "
                              + "on temp.election_id = cabinet.election_id "
                              + "order by extract(year from e_date) DESC;";
    		ps = connection.prepareStatement(getIds);
    		ps.setString(1, countryName);
    		r = ps.executeQuery();

    		// init parameters for looping and final output
    		List<Integer> election_list = new ArrayList<Integer>();
    		List<Integer> cabinet_list = new ArrayList<Integer>();
    		Integer election_id;
    		Integer cabinet_id;

    		// go over the result and add required info into list
    		while (r.next()) {
    			election_id = r.getInt("election_id");
    			cabinet_id = r.getInt("id");
    			election_list.add(election_id);
    			cabinet_list.add(cabinet_id);
    		}
    		r.close();

    		ElectionCabinetResult result = new ElectionCabinetResult(election_list, cabinet_list);

    		System.out.println(result);
    		return result;

    	}catch(SQLException SQLE){
    		System.out.println(SQLE);
    		return null;
    	}
    }

    @Override
    public List<Integer> findSimilarPoliticians(Integer politicianId, Float threshold) {
        // Implement this method!

    	// Init parameters for datebase connection and sql excution
    	PreparedStatement ps;
    	ResultSet r;

    	// try-catch block to handle error cases
    	try{
    		// In this function, we use word info to represent the combination
    		// of comments and descriptions

    		// sql to get info of given president
    		String currentInfo = "select id, description || ' ' || comment as info "
                                   + "from politician_president "
                                   + "where id = ?;";
    		ps = connection.prepareStatement(currentInfo);
    		ps.setInt(1, politicianId);
    		r = ps.executeQuery();

    		String selected = null;
    		if (r.next()) {
    			selected = r.getString("info");
    		}
    		r.close();

    		// sql to get all info of other presidents
    		String otherInfo = "select id, description || ' ' || comment as info "
                                 + "from politician_president "
                                 + "where id != ?;";
    		ps = connection.prepareStatement(otherInfo);
    		ps.setInt(1, politicianId);
    		r = ps.executeQuery();

    		// init parameters for looping and final output
    		String info;
    		Integer id;
    		List<Integer> id_list = new ArrayList<Integer>();

    		// go over all info of other presidents
    		while (r.next()) {
    			id = r.getInt("id");
    			info = r.getString("info");

    			// check similarity of given president and other presidents
    			if (threshold <= similarity(info, selected)) {
    				id_list.add(id);
    			}
    		}

    		System.out.println(id_list);
    		return id_list;

    	}catch(SQLException SQLE){
    		System.out.println(SQLE);
    		return null;
    	}
    }

    public static void main(String[] args) {
        // You can put testing code in here. It will not affect our autotester.

    	Assignment2 a2 = null;

    	// init test case and handle error first
    	try{
    		a2 = new Assignment2();
    	}catch(ClassNotFoundException CNFE){
    		System.out.println("Failed in initialization.");
    		return;
    	}

    	// use my username as a example
    	String url = "jdbc:postgresql://localhost:5432/csc343h-wangz154?currentSchema=parlgov";
    	String username = "wangz154";
    	String password = "";

    	// init inputs
    	Float threshold = 0.0f;
    	Integer politicianId = 9;

    	if (a2.connectDB(url, username, password)) {
    		System.out.println("Connected!");
    	}else{
    		System.out.println("Failed to Connect!");
    	}

    	// test
    	a2.electionSequence("Japan");
    	a2.findSimilarPoliticians(politicianId, threshold);
    }

}
