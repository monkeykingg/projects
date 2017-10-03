package model;

import java.io.File;

/**
 * A file manager based on a root, which organizes all File and corresponding
 * FileNode in the hierarchy.
 */
public class FileManager {
	// Credit: Assignment 1 part 2 codes

	/**
	 * The prefix to use when displaying nested files and directories; child has
	 * one layer of prefix more than its parent .
	 */
	private static String FILE_PREFIX = "--";

	/** The File root on which the file manager is based. */
	private File root;

	/** The FileNode representing the File root. */
	private FileNode rootNode;

	/**
	 * A file manager.
	 *
	 * @param root
	 *            the File root on which the file manager is based (which can be
	 *            a normal file, including a photo, or a directory)
	 * @param rootNode
	 *            the FileNode representing the root
	 */
	public FileManager(File root, FileNode rootNode) {
		// Initialize instance variables
		this.root = root;
		this.rootNode = rootNode;

		// If root is a directory, build the tree of nodes rooted at file in the
		// file system and update rootNode in order to make the hierarchy in the
		// FileManager complete.
		if (root.isDirectory()) {
			buildTree(root, rootNode);
		}
	}

	/**
	 * Return a string of PREFIX.
	 * 
	 * @return the PREFIX
	 */
	public static String getPREFIX() {
		return FILE_PREFIX;
	}

	/**
	 * Set a new string newPrefix to PREFIX.
	 * 
	 * @param newPrefix
	 *            the new prefix to set
	 */
	public static void setPREFIX(String newPrefix) {
		FILE_PREFIX = newPrefix;
	}

	/**
	 * Return the File root on which the file manager is based.
	 * 
	 * @return the root
	 */
	public File getRoot() {
		return root;
	}

	/**
	 * Return the FileNode representing the File root.
	 * 
	 * @return the rootNode
	 */
	public FileNode getRootNode() {
		return rootNode;
	}

	/**
	 * Build the tree of nodes rooted at file in the file system; note curr is
	 * the FileNode corresponding to file, so this only adds nodes for children
	 * of file to the tree. Precondition: file represents a directory.
	 * 
	 * @param file
	 *            the directory we are building
	 * @param curr
	 *            the node representing file
	 */
	public static void buildTree(File file, FileNode curr) {
		// file always represents a directory; deal with items
		// inside the directory if here's any
		File[] contents = file.listFiles();
		for (File item : contents) {
			FileNode child;

			// Instantiate a FileNode corresponding to item; and what's
			// more, if item is also a directory, recursively build the
			// tree of nodes
			if (item.isDirectory()) {
				child = new FileNode(item.getName(), curr, FileType.DIRECTORY);
				buildTree(item, child);
			} else {

				// We don't bother to specify photoNode at this time
				child = new FileNode(item.getName(), curr, FileType.FILE);
			}

			// Add the FileNode corresponding to item as a child of curr
			curr.addChild(child.getName(), child);
		}
	}

	/**
	 * Build a string buffer representation of the contents of the tree rooted
	 * at fileNode, prepending each file name with prefix, and adding and
	 * additional FILE_PREFIX for subdirectory contents.
	 *
	 * @param fileNode
	 *            the root of the subtree
	 * @param contents
	 *            the string to display
	 * @param prefix
	 *            the prefix to prepend
	 */
	public static void buildDirectoryContents(FileNode fileNode, StringBuffer contents, String prefix) {
		// Generate string representation for fileNode
		contents.append(prefix);
		contents.append(fileNode.getName());

		contents.append("\n");

		// If fileNode is a directory, we need to take care of
		// its child nodes (if here's any); otherwise nothing to bother
		if (fileNode.isDirectory()) {
			for (FileNode child : fileNode.getChildren()) {
				buildDirectoryContents(child, contents, prefix + FILE_PREFIX);
			}
		}
	}
}
