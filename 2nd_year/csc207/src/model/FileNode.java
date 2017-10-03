package model;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

/**
 * A root of tree, which represents the directory structure.
 */
public class FileNode {
	// Credit: Assignment 1 part 2 codes

	/**
	 * The name of this FileNode, which represents a non-image file, a image or
	 * a directory.
	 */
	private String name;

	/** This FileNode represents a non-image file, a image or a directory. */
	private FileType type;

	/** This FileNode's parent node. */
	private FileNode parent;

	/**
	 * This FileNode's children, mapped from the file names to the nodes. If
	 * type is FileType.FILE or FileType.IMAGE, this is null.
	 */
	private Map<String, FileNode> children;

	/**
	 * A node in this tree.
	 *
	 * @param name
	 *            the string of name of this FileNode
	 * @param parent
	 *            this FileNode's parent node
	 * @param type
	 *            file, image or directory
	 */
	public FileNode(String name, FileNode parent, FileType type) {
		// Deal with parameters passed in
		this.name = name;
		this.parent = parent;
		this.type = type;

		// If type is Directory, children is a collection;
		// otherwise, children is null
		if (this.isDirectory()) {
			this.children = new HashMap<String, FileNode>();
		} else {
			this.children = null;
		}
	}

	/**
	 * Return the name of the file, image or directory represented by current
	 * node.
	 * 
	 * @return the string of name
	 */
	public String getName() {
		return name;
	}

	/**
	 * Set a new name to this FileNode.
	 * 
	 * @param name
	 *            the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * Return the type of current node.
	 * 
	 * @return the type
	 */
	public FileType getType() {
		return type;
	}

	/**
	 * Return current node's parent node.
	 * 
	 * @return the parent
	 */
	public FileNode getParent() {
		return parent;
	}

	/**
	 * Return the child nodes of current node.
	 * 
	 * @return a collection of children nodes' values
	 */
	public Collection<FileNode> getChildren() {
		return this.children.values();
	}

	/**
	 * Return whether current node represents a directory.
	 * 
	 * @return whether current node represents a directory
	 */
	public boolean isDirectory() {
		return this.type == FileType.DIRECTORY;
	}

	/**
	 * Return whether current node represents an image.
	 * 
	 * @return whether current node represents an image
	 */
	public boolean isPhoto() {
		return this.type == FileType.IMAGE;
	}

	/**
	 * Add childNode, representing a file, a image or directory named name, as a
	 * child of this node.
	 * 
	 * @param name
	 *            the name of the file, image or directory
	 * @param childNode
	 *            the node to add as a child
	 */
	public void addChild(String name, FileNode childNode) {
		this.children.put(name, childNode);
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

		// When dealing with a Directory, we search its child nodes;
		// otherwise directly return null
		if (this.isDirectory()) {
			Collection<FileNode> childNodes = this.getChildren();
			for (FileNode curr : childNodes) {

				// If curr is what we want, immediately return it;
				// otherwise recursively search in child nodes of curr
				if (curr.name.equals(name)) {
					return curr;
				} else {
					result = curr.findChild(name);

					// If we already find what we want in child nodes of curr,
					// we don't bother to do any more search
					if (result != null) {
						return result;
					}
				}
			}
		}
		return result;
	}
}
