package directory_explorer;

import java.util.Map;
import java.util.Collection;
import java.util.HashMap;

/**
 * The root of a tree representing a directory structure.
 */
public class FileNode {

	/** The name of the file or directory this node represents. */
	private String name;
	/** Whether this node represents a file or a directory. */
	private FileType type;
	/** This node's parent. */
	private FileNode parent;
	/**
	 * This node's children, mapped from the file names to the nodes. If type is
	 * FileType.FILE, this is null.
	 */
	private Map<String, FileNode> children;

	/**
	 * A node in this tree.
	 *
	 * @param name
	 *            the file
	 * @param parent
	 *            the parent node.
	 * @param type
	 *            file or directory
	 * @see buildFileTree
	 */
	public FileNode(String name, FileNode parent, FileType type) {
		this.name = name;
		// TODO: complete this method.
		
		// Complete the constructor
		this.parent = parent;
		this.type = type;
		
		// Check children type
		if (type == FileType.DIRECTORY){
			this.children = new HashMap<String, FileNode>();
		}else{
			this.children = null;
		}
	}

	/**
	 * Find and return a child node named name in this directory tree, or null
	 * if there is no such child node.
	 *
	 * @param name
	 *            the file name to search for
	 * @return the node named name
	 */
	public FileNode findChild(String name) {
		FileNode result = null;
		// TODO: complete this method.
		
		// Loop children map
		for (String child : children.keySet()){
			
			// Base case
			if (child.equals(name)){
				
				return children.get(child);
			}
			
			else{
				
				// Create a node to hold recursive solution
				FileNode c = children.get(child).findChild(name);
				if (c != null){
					return c;
				}
			}
		}
		return result;
	}

	/**
	 * Return the name of the file or directory represented by this node.
	 *
	 * @return name of this Node
	 */
	public String getName() {
		return this.name;
	}

	/**
	 * Set the name of the current node
	 *
	 * @param name
	 *            of the file/directory
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * Return the child nodes of this node.
	 *
	 * @return the child nodes directly underneath this node.
	 */
	public Collection<FileNode> getChildren() {
		return this.children.values();
	}

	/**
	 * Return this node's parent.
	 * 
	 * @return the parent
	 */
	public FileNode getParent() {
		return parent;
	}

	/**
	 * Set this node's parent to p.
	 * 
	 * @param p
	 *            the parent to set
	 */
	public void setParent(FileNode p) {
		this.parent = p;
	}

	/**
	 * Add childNode, representing a file or directory named name, as a child of
	 * this node.
	 * 
	 * @param name
	 *            the name of the file or directory
	 * @param childNode
	 *            the node to add as a child
	 */
	public void addChild(String name, FileNode childNode) {
		this.children.put(name, childNode);
	}

	/**
	 * Return whether this node represents a directory.
	 * 
	 * @return whether this node represents a directory.
	 */
	public boolean isDirectory() {
		return this.type == FileType.DIRECTORY;
	}

	/**
	 * This method is for code that tests this class.
	 * 
	 * @param args
	 *            the command line args.
	 */
	public static void main(String[] args) {
		System.out.println("Testing FileNode");
		FileNode f1 = new FileNode("top", null, FileType.DIRECTORY);
		if (!f1.getName().equals("top")) {
			System.out.println("Error: " + f1.getName() + " should be " + "top");
		}
		
		FileNode R = new FileNode("Root", null, FileType.DIRECTORY);
		FileNode c1 = new FileNode("c1", R, FileType.DIRECTORY);
		R.addChild("c1", c1);
		FileNode c2 = new FileNode("c2", R, FileType.DIRECTORY);
		R.addChild("c2", c2);
		FileNode c3 = new FileNode("c3", R, FileType.DIRECTORY);
		R.addChild("c3", c3);
		FileNode g1 = new FileNode("g1", c1, FileType.DIRECTORY);
		c1.addChild("g1", g1);
		FileNode g2 = new FileNode("g2", c1, FileType.FILE);
		c1.addChild("g2", g2);
		FileNode g3 = new FileNode("g3", c3, FileType.DIRECTORY);
		c3.addChild("g3", g3);
		System.out.println(R.findChild("g3").getName());
		System.out.println(R.findChild("g2").getName());
		
	}

}
