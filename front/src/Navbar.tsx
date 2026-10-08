type NavbarProps = {
	title: string;
};

export function Navbar({ title }: NavbarProps) {
	return (
		<nav>
			<h1>{title}</h1>
		</nav>
	);
}
